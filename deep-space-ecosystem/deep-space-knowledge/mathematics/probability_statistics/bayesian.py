"""
Bayesian statistics and posterior probabilities: P(A|B) = P(B|A)*P(A) / P(B).
"""

import numpy as np

def bayes_posterior(prior_a, likelihood_b_given_a, likelihood_b_given_not_a):
    """
    Computes the posterior probability P(A|B) using Bayes' Theorem.
    P(A|B) = P(B|A)*P(A) / ( P(B|A)*P(A) + P(B|¬A)*P(¬A) )
    """
    p_a = prior_a
    p_not_a = 1.0 - prior_a
    
    p_b = likelihood_b_given_a * p_a + likelihood_b_given_not_a * p_not_a
    
    if p_b == 0.0:
        return 0.0
        
    return (likelihood_b_given_a * p_a) / p_b
