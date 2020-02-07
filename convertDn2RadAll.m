%.........Script for converting WV DN's to radiance for all images.........
%Author: James Bramante
%Date: 20/12/2010

close all;
clear all;
clc;

%Define directories for input and output images, if different, the input
%image file extension, and a regular expression for finding the input
%images
path = 'E:\\raw\\vietnam\Danang\satellite\\';
outpath = 'D:\documents\matlab\imageVietnam\';
filext = '.TIF';
regex = ('R[1-7]C[1-3]');

%Create a list of input filenames and iterate through them, converting each
%pixel from digital number expression to absolute radiance (W/(m^2*nm*sr))
cd(path);
list = dir('*.TIF');
for i = 1 : length(list)
    
%     %Load image file and parse filename for output
%     filename = fullfile(path,list(i).name);
%     image = imread(filename);
%     [pathstr, name, ext, versn] = fileparts(filename);
%     ind = regexp(name,regex);
%     [x y z] = size(image);
%     close all;
%     
%     %Keep image as one whole and convert to radiance values
%     name = name(ind:ind+3);
%     image = double(image);
%     image = wvDN2Rad(image);
%     save(fullfile(outpath, name), 'image');
    
    %Split each image in half and convert to radiance values
    image = image(1:ceil(x/2),:,:);
    name1 = strcat(name(ind:ind+3),'upper.mat');
    image = double(image);
    image = wvDN2Rad(image);
    save (fullfile(outpath,name1),'image');
    clear name1 image;
    image = imread(filename);
    close all;
    image = image(ceil(x/2)+1:x,:,:);
    name2 = strcat(name(ind:ind+3),'lower.mat');
    image = double(image);
    image = wvDN2Rad(image);
    save (fullfile(outpath,name2),'image');
    clear name2 image;
end
