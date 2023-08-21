clearvars,clc

%% Received Audio Processing
%% Load Audio Files
clc
% Chirping Bird
[y_received,fs] = audioread('Synthesized_Received_Audio.wav');

% Happy Birthday Original
[y_birthday] = audioread('HappyBirthday.mp3');


y_birthday_true = 0.1*y_birthday; % Some portion of Sound is recorded

% Find Mean Square Error
MSE_1 = MSE(y_birthday_true,y_received);

%% Play Birthday and Received Sounds
% Play Each for 3 seconds with 2 sec pause in between
soundsc(y_birthday(1:3*fs),fs)
pause(3+2)
soundsc(y_received(1:3*fs),fs)

%% Plot Sounds (Time Domain)

t = (0:numel(y_birthday)-1)/fs;
subplot(211)
plot(t,y_birthday)
xlabel('time (sec)')
ylabel('Amplitude')
xlim([0 Inf])
ylim([-1 1])
title('Original Audio (Time Domain)')

subplot(212)
plot(t,y_received)
xlabel('time (sec)')
ylabel('Amplitude')
xlim([0 Inf])
ylim([-1 1])
title('Received Audio (Time Domain)')

%% Plot Sounds (Frequency Domain)

figure
subplot(211)
Freq_Plot_1(y_received,fs);
title('Received Audio (Frequency Domain)')

subplot(212)
Freq_Plot_1(y_birthday,fs);
title('Original Audio (Frequency Domain)')

%% Remove 50 Hz Grid Interference
[b,a] = butter(4,200/(fs/2),'high');
figure
freqz(b,a,[],fs)
title('50 Hz Grid Interference Removal Filter');

y_filt1 = filtfilt(b,a,y_received); % Zero Phase Filtering

figure
subplot(211)
plot(t,y_filt1)
xlabel('time (sec)')
ylabel('Amplitude')
xlim([0 Inf])
ylim([-1 1])
title('Grid Noise Filtered Audio (Time Domain)')

subplot(212)
Freq_Plot_1(y_filt1,fs);
title('Grid Noise Filtered Audio (Frequency Domain)')

% Find Mean Square Error
MSE_2 = MSE(y_birthday_true,y_filt1);
%% Remove Bird Chirp Interference
[b,a] = butter(4,4000/(fs/2),'low');
figure
freqz(b,a,[],fs)
title('Bird Chirp Removal Filter');

y_filt2 = filtfilt(b,a,y_filt1);

figure
subplot(211)
plot(t,y_filt2)
xlabel('time (sec)')
ylabel('Amplitude')
xlim([0 Inf])
ylim([-1 1])
title('Brid Chirp Interference Filtered Audio (Time Domain)')

subplot(212)
Freq_Plot_1(y_filt2,fs);
title('Brid Chirp Interference Filtered Audio (Frequency Domain)')

% Find Mean Square Error
MSE_3 = MSE(y_birthday_true,y_filt2);
%% Audio Echo Detection
 % Find Correlation for Echo Detection
 
[R, lags] = xcorr(y_filt2, 'unbiased');
R = R(lags > 0);
lags = lags(lags > 0);
figure
plot(lags, R)
title('Auto Correlation')
xlabel('Samples')

[peaks, delta] = findpeaks(R, lags, 'MinPeakHeight', 3e-4);

a = 0.9;  % any random value between zero and one
den = zeros(1,max(delta));
den(1) = 1;
den(delta) = a;
num = 1;

%% Audio Echo Removal
Echo_Removed_Signal = filter(num,den,y_filt2);
figure
subplot(211)
plot(t,Echo_Removed_Signal)
xlabel('time (sec)')
ylabel('Amplitude')
xlim([0 Inf])
ylim([-1 1])
title('Echo Removed Signal Audio (Time Domain)')

subplot(212)
Freq_Plot_1(Echo_Removed_Signal,fs);
title('Echo Removed Signal Audio (Frequency Domain)')
%% Play Recovered Sound
soundsc(Echo_Removed_Signal(1:5*fs),fs)
%% Find Mean Square Error of Recovered Sound
% Find Mean Square Error
MSE_4 = MSE(y_birthday_true,Echo_Removed_Signal);

%% Plot all Mean Square Errors
plot([MSE_1 MSE_2 MSE_3 MSE_4],'-O','MarkerFaceColor','y','Linewidth',2)
ylabel('Mean Square Error')
title('MSE at Each Processing Step')
xticks([1:4]);
xticklabels({'MSE @ Received Signal','MSE after 50 Hz Removal','MSE after Bird Chirp Removal','MSE after Echo Removal'});
ax = gca;
ax.FontSize = 12;

%% Write Recovered Audio as Wav File
clc
audiowrite('Recovered_Received_Audio.wav',Echo_Removed_Signal,fs);