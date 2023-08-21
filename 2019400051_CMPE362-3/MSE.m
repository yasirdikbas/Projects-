function [y_error] = MSE(inputArg1,inputArg2)

y_error = 0;

L = numel(inputArg1);
for N = 1:L
y_error = y_error + ((inputArg1(N)-inputArg2(N)).^2);
end
y_error = y_error/L;
end

