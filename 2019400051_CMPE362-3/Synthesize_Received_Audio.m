clearvars,clc

%% Audio Sythesis
%% Load Clean Audio Files
clc
% Chirping Bird
[y_bird,fs] = audioread('Bird_Chirping.mp3');

% Happy Birthday
[y_birthday] = audioread('HappyBirthday.mp3');

%% Make Length Same

% Birds Chirp is shorter so repeat to make same length

len_diff = numel(y_birthday)/numel(y_bird);

y_bird_rep = repmat(y_bird,floor(len_diff),1);
y_bird_rep = [y_bird_rep;y_bird(1:numel(y_birthday)-numel(y_bird_rep))];

%% Play Birthday and Bird Chirp Sounds

% Play Each for 3 seconds with 2 sec pause in between

sound(y_birthday(1:3*fs),fs)
pause(3+2)
sound(y_bird_rep(1:3*fs),fs)

%% Create 50 Hz Electrical Grid Interference

t = (0:numel(y_birthday)-1)/fs;
f = 50;

grid_amp = 1;
y_grid = cos(2*pi*f*t');

%% Plot Sounds (Time Domain)
clc

subplot(311)
plot(t,y_birthday)
xlabel('time (sec)')
ylabel('Amplitude')
xlim([0 Inf])
ylim([-1 1])
title('Birthday Audio (Time Domain)')

subplot(312)
plot(t,y_bird_rep)
xlabel('time (sec)')
ylabel('Amplitude')
xlim([0 Inf])
ylim([-1 1])
title('Bird Audio (Time Domain)')

subplot(313)
plot(t,y_grid)
xlabel('time (sec)')
ylabel('Amplitude')
xlim([0 Inf])
ylim([-1 1])
title('50 Hz Grid Interference (Time Domain)')

%% Plot Sounds (Frequency Domain)
clc

figure
subplot(311)
Freq_Plot_1(y_birthday,fs);
title('Birthday Audio (Frequency Domain)')

subplot(312)
Freq_Plot_1(y_bird_rep,fs);
title('Bird Audio (Frequency Domain)')

subplot(313)
Freq_Plot_1(y_grid,fs);
title('50 Hz Grid Interference (Frequency Domain)')

%% Simulate Echo
clc
distance_echo = 30; % meters
c = 340;
time_delay = 2*distance_echo/c;
samples_delay = round(time_delay*fs);

echo_amp = 1;
echo_birthday = echo_amp*[zeros(samples_delay,1);y_birthday(1:end-samples_delay)];

figure
plot(t,y_birthday,t,echo_birthday)
xlabel('time (sec)')
ylabel('Amplitude')
xlim([0 Inf])
ylim([-1 1])
title('Birthday and Echo Audio (Time Domain)')
legend('Original','Echo')

%% Synthesize Audio

% Add all interferences (Birds Chirp, and Grid) and Echo

audio_scaling = 0.1;
received_audio = audio_scaling*(y_birthday + echo_birthday + 0.5*y_bird_rep + y_grid);

figure
subplot(211)
plot(t,received_audio)
xlabel('time (sec)')
ylabel('Amplitude')
xlim([0 Inf])
ylim([-1 1])
title('Received Audio (Time Domain)')

subplot(212)
Freq_Plot_1(received_audio,fs);
title('Received Audio (Frequency Domain)')

%% Play Synthesized Received Audio

% Play for 4 seconds
sound(received_audio(1:4*fs),fs)

%% Write Synthesized Received Audio as Wav File
clc
audiowrite('Synthesized_Received_Audio.wav',received_audio,fs);
