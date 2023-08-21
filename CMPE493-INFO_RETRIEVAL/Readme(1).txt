The algorithm is designed to work on any data similar to the provided, as long as it's in the .txt format.

To use your own data, you need to modify the file path of the "data.txt" file in the code. This is quite straightforward. 

Let's say, for instance, your "data.txt" file is located in the directory 'content/data.txt'.

Look for the following piece of code in your program:
vertices, edges = read_data('/content/drive/MyDrive/Colab Notebooks/data.txt') # Reading data from 'data.txt' file

Here, '/content/drive/MyDrive/Colab Notebooks/data.txt' is the current path that the program is using to read the data.

You need to replace it with the path of your "data.txt" file. So, after replacement, the code would look like:
vertices, edges = read_data('content/data.txt') # Reading data from 'data.txt' file

By doing this, you're instructing the program to read the data from your specified .txt file instead of the default one.

Remember: The path you provide should correspond to the location where your "data.txt" file is stored.
