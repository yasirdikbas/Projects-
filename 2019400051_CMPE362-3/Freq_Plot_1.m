function [Y_axis,X_axis]=Freq_Plot_1(signal,samplingFreq)
L=length(signal);
Y_axis=fftshift(abs(fft(signal)))/L;
X_axis=(-L/2:L/2-1)*samplingFreq/L;
plot(X_axis,20*log10(Y_axis))
xlabel('Frequency (Hz)')
ylabel('Amplitude (dB)')
end