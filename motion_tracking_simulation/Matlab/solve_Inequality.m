syms x
ineq = x^4 +7*x -3*x^3 -6 > 0;
S = solve(ineq, x,'IgnoreAnalyticConstraints', true, 'MaxDegree', 4, 'Real', true, 'ReturnConditions', true)
