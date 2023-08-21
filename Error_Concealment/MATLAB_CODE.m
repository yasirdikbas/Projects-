%% 
% 

clearvars
close all
clc
s = rng(1); %% Set the random seed for reproducibility

%% Select and Read the Image

% Uncomment the selected image
img1 = imread("dog.png");
% img1 = imread("cat.png");
% img1 = imread("otter.png");


% Convert to Gray Scale
img1_gray = rgb2gray(img1);
img_size = size(img1_gray);

figure
imshow(img1_gray)
title('Original Gray Scale Image');
%% Set range of values of most significant bits n and corrupted rows info
n = 2:5;

% Set the number and starting index of corrupted rows
num_corr_rows = 30;
start_corr_row = 51;
%% Initialize RMSEs Array

RMSEs = zeros(3,numel(n)); % three RMSE for each n

%% Loop through all n values and find comparisons
for bits = 1:numel(n)
    % Downsample and Concatenate Image    
    % downsample
    img1_downsampled = img1_gray(1:2:img_size(1),1:2:img_size(2));
    
    % concatenate
    img1_concat = [img1_downsampled img1_downsampled;
        img1_downsampled img1_downsampled];
    
    
    % Calculate Transmitted Image
    transmitted_img = uint8(zeros(img_size));
    
    for i = 1:img_size(1)
        for j = 1:img_size(2)
            % Concatenated Image
            % Pick the pixel level
            pixel_concat = img1_concat(i,j);
            % Convert to 8 bit binary
            binary_pixel_concat = dec2bin(pixel_concat,8);
            % Hide concatenated image in least sig bits
            binary_pixel_clipped_concat = [repmat('0',1,8-n(bits)) binary_pixel_concat(1:n(bits))];
            % Convert Binary to decimal
            pixel_clipped_concat = bin2dec(binary_pixel_clipped_concat);
            
            % Original GrayScale Image
            % Pick the pixel level
            pixel_orig = img1_gray(i,j);
            % Convert to 8 bit binary
            binary_pixel_orig = dec2bin(pixel_orig,8);
            % Limit value to 8-n most sig bits
            binary_pixel_clipped_orig = [binary_pixel_orig(1:8-n(bits)) repmat('0',1,n(bits)) ];
            % Convert Binary to decimal
            pixel_clipped_orig = bin2dec(binary_pixel_clipped_orig);
            
            % Add both values to form one pixel level
            pixel = pixel_clipped_orig + pixel_clipped_concat;
            % Add into transmitted signal image
            transmitted_img(i,j) = pixel;
        end
    end
    
    % Third Root Mean Square Error
    RMSEs(1,bits) = sqrt(sum((transmitted_img - img1_gray).^2,'all')/numel(img1));
    
    % Manually Add Error
    
    rng(s); % Use same random seed
    corrupted_rows = uint8(round(rand(30,img_size(2))*255)); % Add rand error
    
    transmitted_img_corrupted = transmitted_img;
    transmitted_img_corrupted(start_corr_row:start_corr_row + num_corr_rows - 1,:) = corrupted_rows;
    
    % Second Root Mean Square Error
    RMSEs(2,bits) = sqrt(sum((transmitted_img_corrupted - img1_gray).^2,'all')/numel(img1));
    
    % Find and Replace Corrupted Pixels with Downsampled Image Quadrant
    % Find row indexes of uncorrupted pixels for replacing corrupting ones
    uncorrupted_copy_indexes = round((start_corr_row/2 + img_size(1)/2):(start_corr_row/2 + num_corr_rows/2 - 1 + img_size(1)/2));
    
    neat_downsampled_copy = uint8(zeros(num_corr_rows/2,img_size(2)/2));
    % Find and Replace Corrupted Rows with Downsampled Copy
    for i = 1:num_corr_rows/2
        for j = 1:img_size(2)/2
            neat_row = uncorrupted_copy_indexes(i);
            if(neat_row > img_size(1)) % Avoid Overflow
                neat_row = neat_row - 256;
            end
            pixel_neat = transmitted_img_corrupted(neat_row,j);
            binary_pixel_neat = dec2bin(pixel_neat,8); % Convert to binary
            
            % Find in least sig bits and shift bits to orig position
            binary_pixel_neat_downsampled = [binary_pixel_neat((end-n(bits)+1):end) repmat('0',1,8-n(bits)) ];
            pixel_neat_downsampled = bin2dec(binary_pixel_neat_downsampled);
            % No info of end bits so add mean value
            neat_downsampled_copy(i,j) = pixel_neat_downsampled + floor(bin2dec(repmat('1',1,8-n(bits)))/2);
        end
    end
    % Upsample to Original Size and Replace values of Corrupted Pixels
    % Find Recovered Signal
    neat_downsampled_copy_upsampled = repelem(neat_downsampled_copy,2,2);
    
    replaced_corrupted = transmitted_img_corrupted;
    % Replace Corrupted Rows
    replaced_corrupted(start_corr_row:start_corr_row + num_corr_rows - 1,:) = neat_downsampled_copy_upsampled;
    
    % Remove least sig bits of concatenated images
    for i = [1:(start_corr_row-1) (start_corr_row + num_corr_rows):img_size(1)]
        for j = 1: img_size(2)
            pixel_neat = replaced_corrupted(i,j);
            binary_pixel_neat = dec2bin(pixel_neat,8);
            binary_pixel_neat_clipped = [binary_pixel_neat(1:8-n(bits)) repmat('0',1,n(bits))];
            pixel_neat_clipped = bin2dec(binary_pixel_neat_clipped) + floor(bin2dec(repmat('1',1,n(bits)))/2);
            replaced_corrupted(i,j) = pixel_neat_clipped;
        end
    end
    
    % Third Root Mean Square Error
    RMSEs(3,bits) = sqrt(sum((replaced_corrupted - img1_gray).^2,'all')/numel(img1));
    disp(['Done for n = ' num2str(n(bits))]);
end

%%
num_of_bits = n';
RMSE_1 = RMSEs(1,:)';
RMSE_2 = RMSEs(2,:)';
RMSE_3 = RMSEs(3,:)';
T = table(num_of_bits,RMSE_1,RMSE_2,RMSE_3)

figure
plot(T.num_of_bits,T.RMSE_1,'-o','MarkerFaceColor','r')
title('Num of bits vs Root Mean Square Error 1')
xlabel('Number of bits');
ylabel('Root Mean Square Error 1');

figure
plot(T.num_of_bits,T.RMSE_2,'-o','MarkerFaceColor','r')
title('Num of bits vs Root Mean Square Error 2')
xlabel('Number of bits');
ylabel('Root Mean Square Error 2');

figure
plot(T.num_of_bits,T.RMSE_3,'-o','MarkerFaceColor','r')
title('Num of bits vs Root Mean Square Error 3')
xlabel('Number of bits');
ylabel('Root Mean Square Error 3');