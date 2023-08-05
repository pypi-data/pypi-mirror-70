# Copyright (c) Dietmar Wolz.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory.

import random
import time
import math
import os
import ctypes as ct
import numpy as np
from numpy.random import Generator, MT19937, SeedSequence
from scipy.optimize._constraints import new_bounds_to_old
from scipy.optimize import OptimizeResult, Bounds
import multiprocessing as mp
from multiprocessing import Process
from fcmaes.optimizer import de_cma, dtime

os.environ['MKL_DEBUG_CPU_TYPE'] = '5'
os.environ['MKL_NUM_THREADS'] = '1'
os.environ['OPENBLAS_NUM_THREADS'] = '1'

def minimize(fun, 
             bounds = None, 
             value_limit = math.inf,
             num_retries = 1000,
             logger = None,
             workers = mp.cpu_count(),
             popsize = 31, 
             max_evaluations = 50000, 
             stop_fittness = None,
             optimizer = None,
             ):   
    """Minimization of a scalar function of one or more variables using parallel 
     CMA-ES retry.
     
    Parameters
    ----------
    fun : callable
        The objective function to be minimized.
            ``fun(x, *args) -> float``
        where ``x`` is an 1-D array with shape (n,) and ``args``
        is a tuple of the fixed parameters needed to completely
        specify the function.
    bounds : sequence or `Bounds`, optional
        Bounds on variables. There are two ways to specify the bounds:
            1. Instance of the `scipy.Bounds` class.
            2. Sequence of ``(min, max)`` pairs for each element in `x`. None
               is used to specify no bound.
    value_limit : float, optional
        Upper limit for optimized function values to be stored. 
    num_retries : int, optional
        Number of optimization retries.    
    logger : logger, optional
        logger for log output of the retry mechanism. If None, logging
        is switched off. Default is a logger which logs both to stdout and
        appends to a file ``optimizer.log``.
    workers : int, optional
        number of parallel processes used. Default is mp.cpu_count()
    popsize = int, optional
        CMA-ES population size used for all CMA-ES runs. 
        Not used for differential evolution. 
        Ignored if parameter optimizer is defined. 
    max_evaluations : int, optional
        Forced termination of all optimization runs after ``max_evaluations`` 
        function evaluations. Only used if optimizer is undefined, otherwise
        this setting is defined in the optimizer. 
    stop_fittness : float, optional 
         Limit for fitness value. optimization runs terminate if this value is reached. 
    optimizer : optimizer.Optimizer, optional
        optimizer to use. Default is a sequence of differential evolution and CMA-ES.
     
    Returns
    -------
    res : scipy.OptimizeResult
        The optimization result is represented as an ``OptimizeResult`` object.
        Important attributes are: ``x`` the solution array, 
        ``fun`` the best function value, ``nfev`` the number of function evaluations,
        ``success`` a Boolean flag indicating if the optimizer exited successfully. """

    if optimizer is None:
        optimizer = de_cma(max_evaluations, popsize, stop_fittness)        
    store = Store(bounds, logger = logger)
    return retry(fun, store, optimizer.minimize, num_retries, value_limit, workers)
                 
def retry(fun, store, optimize, num_retries, value_limit = math.inf, workers=mp.cpu_count()):
    sg = SeedSequence()
    rgs = [Generator(MT19937(s)) for s in sg.spawn(workers)]
    proc=[Process(target=_retry_loop,
            args=(pid, rgs, fun, store, optimize, num_retries, value_limit)) for pid in range(workers)]
    [p.start() for p in proc]
    [p.join() for p in proc]
    store.sort()
    store.dump()
    return OptimizeResult(x=store.get_x_best(), fun=store.get_y_best(), 
                          nfev=store.get_count_evals(), success=True)
 
class Store(object):
    """thread safe storage for optimization retry results."""
       
    def __init__(self, 
                 bounds, # bounds of the objective function arguments
                 check_interval = 10, # sort evaluation memory after check_interval iterations
                 capacity = 500, # capacity of the evaluation store
                 logger = None # if None logging is switched off
                ):    
        self.lower, self.upper = _convertBounds(bounds)
        self.logger = logger
        self.capacity = capacity
        self.check_interval = check_interval
        self.dim = len(self.lower)
        self.delta = []
        for k in range(self.dim):
            self.delta.append(self.upper[k] - self.lower[k])
        
        #shared between processes
        self.add_mutex = mp.Lock()    
        self.xs = mp.RawArray(ct.c_double, self.capacity * self.dim)
        self.ys = mp.RawArray(ct.c_double, self.capacity)  
        self.count_evals = mp.RawValue(ct.c_long, 0)   
        self.count_runs = mp.RawValue(ct.c_int, 0) 
        self.num_stored = mp.RawValue(ct.c_int, 0) 
        self.num_sorted = mp.RawValue(ct.c_int, 0)  
        self.count_stat_runs = mp.RawValue(ct.c_int, 0)  
        self.t0 = time.perf_counter()
        self.mean = mp.RawValue(ct.c_double, 0) 
        self.qmean = mp.RawValue(ct.c_double, 0) 
        self.best_y = mp.RawValue(ct.c_double, math.inf) 
        self.best_x = mp.RawArray(ct.c_double, self.dim)
    
    def eval_num(self, max_evals):
        return max_evals
                                             
    def replace(self, i, y, xs):
        self.set_y(i, y)
        self.set_x(i, xs)
             
    def sort(self): # sort all entries to make room for new ones, determine best and worst
        """sorts all store entries, keep only the 90% best to make room for new ones."""
        ns = self.num_stored.value
        ys = np.asarray(self.ys[:ns])
        yi = ys.argsort()
        sortRuns = []
        for i in range(len(yi)):
            y = ys[yi[i]]
            xs = self.get_x(yi[i])
            sortRuns.append((y, xs))
        numStored = min(len(sortRuns),int(0.9*self.capacity)) # keep 90% best 
        for i in range(numStored):
            self.replace(i, sortRuns[i][0], sortRuns[i][1])
        self.num_sorted.value = numStored  
        self.num_stored.value = numStored  
        return numStored        
            
    def add_result(self, y, xs, evals, limit=math.inf):
        """registers an optimization result at the score."""
        with self.add_mutex:
            self.incr_count_evals(evals)
            if y < limit:  
                self.count_stat_runs.value += 1
                if y < self.best_y.value:
                    self.best_y.value = y
                    self.best_x[:] = xs[:]
                    self.dump()
                if self.num_stored.value >= self.capacity-1:
                    self.sort()
                cnt = self.count_stat_runs.value
                diff = y - self.mean.value
                self.qmean.value += (cnt - 1) * diff*diff / cnt;
                self.mean.value += diff / cnt
                ns = self.num_stored.value
                self.num_stored.value = ns + 1
                self.replace(ns, y, xs)
            
    def get_x(self, pid):
        return self.xs[pid*self.dim:(pid+1)*self.dim]

    def get_x_best(self):
        return self.best_x[:]
    
    def get_y(self, pid):
        return self.ys[pid]

    def get_y_best(self):
        return self.best_y.value
    
    def get_ys(self):
        return self.ys[:self.num_stored.value]
             
    def get_y_mean(self):
        return self.mean.value

    def get_y_standard_dev(self):
        cnt = self.get_count_runs()
        return 0 if cnt <= 0 else math.sqrt(self.qmean.value / cnt)

    def get_count_evals(self):
        return self.count_evals.value
 
    def get_count_runs(self):
        return self.count_runs.value
 
    def set_x(self, pid, xs):
        self.xs[pid*self.dim:(pid+1)*self.dim] = xs[:]
       
    def set_y(self, pid, y):
        self.ys[pid] = y    
 
    def get_runs_compare_incr(self, limit):
        with self.add_mutex:
            if self.count_runs.value < limit:
                self.count_runs.value += 1
                return True
            else:
                return False 
       
    def incr_count_evals(self, evals):
        if self.count_runs.value % self.check_interval == self.check_interval-1:
            self.sort()
        self.count_evals.value += evals
            
    def dump(self):
        """logs the current status of the store if logger defined."""
        if self.logger is None:
            return
        Ys = self.get_ys()
        vals = []
        for i in range(min(20, len(Ys))):
            vals.append(round(Ys[i],2))     
        dt = dtime(self.t0)   
                 
        message = '{0} {1} {2} {3} {4:.6f} {5:.2f} {6:.2f} {7!s} {8!s}'.format(
            dt, int(self.count_evals.value / dt), self.count_runs.value, self.count_evals.value, \
                self.best_y.value, self.get_y_mean(), self.get_y_standard_dev(), vals, self.best_x[:])
        self.logger.info(message)

        
def _retry_loop(pid, rgs, fun, store, optimize, num_retries, value_limit):
    lower = store.lower
    while store.get_runs_compare_incr(num_retries):        
        try:       
            sol, y, evals = optimize(fun, Bounds(store.lower, store.upper), None, 
                                     [random.uniform(0.05, 0.1)]*len(lower), rgs[pid], store)
            store.add_result(y, sol, evals, value_limit)           
        except Exception as ex:
            continue
#         if pid == 0:
#             store.dump()

def _convertBounds(bounds):
    if bounds is None:
        raise ValueError('bounds need to be defined')
    if isinstance(bounds, Bounds):
        limits = np.array(new_bounds_to_old(bounds.lb,
                                                 bounds.ub,
                                                 len(bounds.lb)),
                               dtype=float).T
    else:
        limits = np.array(bounds, dtype='float').T
    if (np.size(limits, 0) != 2 or not
            np.all(np.isfinite(limits))):
        raise ValueError('bounds should be a sequence containing '
                         'real valued (min, max) pairs for each value'
                         ' in x')
    return limits[0], limits[1]
