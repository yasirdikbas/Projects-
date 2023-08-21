#include <iostream>
#include <exception>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <set>
#include <map>
#include <cmath>
#include <mutex>
#include <thread>
// used to set floating point precision:
#include <iomanip>
// used for sorting and set ops:
#include <algorithm>
//Author Yasir Dikbaş
// Some global program data, here are some of the parameters from
// the input file and command line arguments.
std::string inputFilename, outputFilename;
unsigned int numThreads, numAbstractsToScan, numAbstractsToReturn;

// All names of abstract files we will scan
// This is a shared resource
std::vector<std::string> abstractFilenames;
std::mutex abstractFilenamesMutex;

// The words of the query, represented in a set
// This resource will be shared, but only for read operations
// so a mutex is not strictly necessary
std::set<std::string> queryWords;

// File stream to the output file with name
// listed in the command line arguments.
// Multiple threads will write to this file so we must provide a
// corresponding mutex.
std::ofstream logFile;
std::mutex logFileMutex;

// A data structure representing the data associated with an 
// abstract
struct AbstractFileData
{
    // the individual sentences from the file
    std::vector<std::string> sentences;
    // map each sentence to its corresponding Jaccane score
    std::map<std::string, double> sentenceScores;
    // the Jaccane score for the entire abstract
    double overallScore;
    // the original filename, for output purposes
    std::string name;
};

// The "pile of work" that the threads will add to,
// items in this vector will have all fields populated
// so that they can be outputted.
// This is a shared resource so we must provide a corresponding
// mutex
std::vector<AbstractFileData> resultData;
std::mutex resultDataMutex;

// A list of exceptions thrown in worker threads.
// This is a shared resource so we must provide a corresponding
// mutex.
std::vector<std::exception> exceptionStack;
std::mutex exceptionStackMutex;

// Takes the command line arguments and attempts to extract
// the program paramters such as:
// 1: the input file name (string)
// 2: the output file name (string)
bool handleCommandlineArguments(int argc, const char* const argv[])
{
    //std::cout << "Handling command line arguments..." << std::endl;
    // Basic argument count check, useful for debugging
    if(argc != 3)
    {
        std::cerr << "Usage: abstractor.out <input file> <output file>" << std::endl;
        return false;
    }
    else
    {
        inputFilename = argv[1];
        outputFilename = argv[2];
        // Try to open the logfile so that it can be used 
        // by the rest of the program
        logFile.open(outputFilename, std::ios::out);
        if(!logFile.good())
            throw std::runtime_error(std::string("Unable to open file: ") + outputFilename);
        //std::cout << "inputFilename: " << inputFilename << "\noutputFilename: " << outputFilename << "\n\n";
        return true;
    }
}

// Utility function for splitting strings by
// a specified delimiter
std::vector<std::string> split(std::string str, char delim)
{
    // somewhere to store the final collection of strings
    std::vector<std::string> result;
    // a buffer which will be used to store the current
    // string encountered before a delimiter
    std::vector<char> buffer;

    for(char c : str)
    {
        // if we've reached the delimiter,
        // add the contents of the buffer as a result
        // (if the buffer is empty, don't bother)
        if(c == delim && buffer.size() > 0)
        {
            // add the null character to the buffer
            // so that it can be processed as a cstring
            buffer.push_back('\0');
            result.push_back(std::string(buffer.data()));
            // reset the buffer so we can keep using it
            buffer.clear();
        }
        // we only add characters to the buffer if they are
        // NOT the specified delimiter
        else if(c != delim)
        {
            buffer.push_back(c);
        }
    }
    // the buffer may have something left over inside,
    // so add the last result if so.
    if(buffer.size() > 0)
    {
        buffer.push_back('\0');
        result.push_back(std::string(buffer.data()));
    }
    return result;
}

// utility function for removing all instances
// of a given character from a string
std::string remove(std::string str, char r)
{
    std::string result;
    for(char c : str)
        if(c != r)
            result += c;
    return result;
}

// takes the name of an "input file" and processes it.
// an input file is the file which describes the parameters
// of the Abstractor
// the parameters in the input file will be extracted
// and made global for use throughout the program
bool processInputFile(std::string filename)
{
    //std::cout << "Processing input file...\nfilename: " << filename << std::endl;
    try
    {
        std::ifstream file(filename);
        
        // fetch the first line so we can take the
        // simple numerical parameters
        std::string firstLine;
        std::getline(file, firstLine);

        // split the parameters into individual strings
        std::vector<std::string> parameterStrings = split(firstLine, ' ');

        // make the parameters globally available
        numThreads = std::stoul(parameterStrings[0]);
        numAbstractsToScan = std::stoul(parameterStrings[1]);
        numAbstractsToReturn = std::stoul(parameterStrings[2]);

        //std::cout << "numThreads: " << numThreads << "\nnumAbstractsToScan: " << numAbstractsToScan << "\nnumAbstractsToReturn: " << numAbstractsToReturn << std::endl;

        // fetch the second line containing the
        // query words
        std::string secondLine;
        std::getline(file, secondLine);

        // split the line by spaces to get
        // a vector containing these words
        std::vector<std::string> queryWordsList = split(secondLine, ' ');

        //std::cout << "Number of query words: " << queryWordsList.size() << std::endl;

        //std::cout << "queryWords: {";

        // populate the global set with the query words
        for(std::string s : queryWordsList)
        {
            //std::cout << s << ",";
            queryWords.insert(s);
        }

        //std::cout << "}" << std::endl;

        // read the filenames of the abstract
        // files to scan
        for(unsigned int i = 0; i < numAbstractsToScan; i++)
        {
            std::string abstractFilename;
            std::getline(file, abstractFilename);
            abstractFilenames.insert(abstractFilenames.begin(), abstractFilename);
            //std::cout << "abstractFileNames[" << i << "]: " << abstractFilename << std::endl;
        }

        //std::cout << std::endl;

        file.close();

        return true;
    }
    catch(std::exception e)
    {
        std::cerr << e.what();
        return false;
    }
}

// this function will the filename of an abstract
// file and will process it. this involves reading
// all of its lines and splitting these lines into
// individual sentences.
// We will mutate the AbstractFileData passed in by
// reference so we can return the operation's success
bool processAbstractFile(std::string filename, AbstractFileData& data)
{
    //std::cout << "Processing abstract file...\nfilename: " << filename << std::endl;
    try
    {
        std::ifstream file(filename);

        // throw an exception if we couldn't open the file
        if(!file.good())
            throw std::runtime_error(std::string("Unable to open file: ") + filename);

        // initialize a raw buffer to read the file into
        char* buffer = nullptr;
        size_t fileSize;

        // seek to the end of the file stream so we can determine the size
        // of the file and the amount of memory we must allocate to our buffer
        file.seekg(0, std::ios::end);
        fileSize = file.tellg();
        // allocate an extra char of data so we can add the null character
        // to the end of the string. This is necessary as we will convert
        // the buffer to a std::string.
        buffer = new char[fileSize+1];
        buffer[fileSize] = '\0';
        file.seekg(0);
        file.read(buffer, fileSize);
        file.close();
        // copy data from buffer into std::string
        std::string bufferString = buffer;
        // free memory allocated to buffer
        delete[] buffer;

        // split the data in the file into sentences, delimited by period
        std::vector<std::string> sentencesRaw = split(bufferString, '.');

        unsigned int i = 0;
    
        for(std::string sentenceRaw : sentencesRaw)
        {
            // remove any trailing space character
            if(sentenceRaw.front() == ' ')
                sentenceRaw = sentenceRaw.substr(1);
            // remove any newlines that are still in the string
            sentenceRaw = remove(sentenceRaw, '\n');
            // re-add the period which was removed by the split function
            data.sentences.push_back(sentenceRaw + '.');
            //std::cout << "data.sentences[" << i << "]: " << data.sentences[i] << std::endl;
            i++;
        }

        //std::cout << std::endl;

        return true;
    }
    catch(std::runtime_error e)
    {
        std::cerr << e.what();
        return false;
    }
    catch(std::exception e)
    {
        std::cerr << e.what() << std::endl;
        return false;
    }
}


// a utility function which returns a set of words from a sentence
std::set<std::string> getWords(std::string sentence)
{
    // begin by splitting words by space character
    std::vector<std::string> words = split(sentence, ' ');
    // convert vector to set by simple insertion
    std::set<std::string> wordsSet;
    for(auto str : words)
        wordsSet.insert(str);
    return wordsSet;
}


// calculate the Jaccane similiarity score using std::set to easily
// deal with duplicates
double calculateSimilarityScore(std::set<std::string> queryWords, std::set<std::string> words)
{
    // an std::vector representing a union between the two sets
    std::vector<std::string> unionList;
    std::set_union(queryWords.begin(), queryWords.end(), words.begin(), words.end(), std::back_inserter(unionList));
    // an std::vector representing an intersection between the two sets
    std::vector<std::string> intersectionList;
    std::set_intersection(queryWords.begin(), queryWords.end(), words.begin(), words.end(), std::back_inserter(intersectionList));

    //conversion to std::set to remove duplicates
    std::set<std::string> intersectionSet, unionSet;

    for(std::string s : unionList)
        unionSet.insert(s);

    for(std::string s : intersectionList)
        intersectionSet.insert(s);

    // calculate set cardinality for use with the Jaccane formula
    double intersectionCount = (double)intersectionSet.size(), unionCount = (double)unionSet.size();
    // perform the calculation, along with a mathematical trick to round the
    // 4th value after the decimal point.
    return std::round(10000.0*(intersectionCount / unionCount)) / 10000.0;
}


// write the lines to the logfile (the final output .txt)
void logLine(std::string line)
{
    // initialize a lock guard as the logfile is a shared resource
    const std::lock_guard<std::mutex> logFileLock(logFileMutex);
    logFile << line << std::endl;
    // flush the log file in case the program terminates
    // unexpectedly and the buffer is lost
    logFile.flush();
    // lock_guard falls out of scope
}

// the work function for our threads
// pass in a name so that the thread can report its
// actions (Thread A/B/C/...)
void threadLoop(std::string name)
{
    // interrupt flag to break out of work loop
    bool continueWorking = true;
    try
    {
        do
        {
            // we will need to try to access the list of file names to scan
            // so we must lock the mutex
            abstractFilenamesMutex.lock();
            if(abstractFilenames.size() != 0)
            {
                // there is more work to do, so make this thread do it:

                // get the name of the next abstract file to process
                std::string nextFile = abstractFilenames.back();
                // pop this filename from the list so that it does not get processed again
                abstractFilenames.pop_back();
                // unlock the mutex, as we are finished with the resource
                abstractFilenamesMutex.unlock();

                // log our actions to the output file
                logLine(std::string("Thread ") + name + std::string(" is calculating ") + nextFile);

                // initialize the data structure to store the results
                AbstractFileData data;
                // process the requested abstract file and populate the
                // AbstractFileData data structure
                processAbstractFile("../abstracts/" + nextFile, data);

                // get the list of strings which represents the sentences
                auto sentences = data.sentences;
                // store the original filename of the abstract file
                data.name = nextFile;

                // all words in the file, held in a set
                std::set<std::string> allWords;

                for(std::string sentence : sentences)
                {
                    // get the words in the sentence
                    auto words = getWords(sentence);
                    for(auto it = words.begin(); it != words.end(); it++)
                    {
                        // add it to the set of all words for the file
                        allWords.insert(*it);
                    }
                    // calculate the sentence score for the individual sentence,
                    // and map it accordingly
                    double sentenceScore = calculateSimilarityScore(words, queryWords);
                    data.sentenceScores[sentence] = sentenceScore;
                }
                // now, with a fully populated set of words for the entire
                // abstract, we can calculate the overall score
                double overallScore = calculateSimilarityScore(allWords, queryWords);
                // populate the result to the data structure
                data.overallScore = overallScore;
                // we are now ready to submit the work, so we lock the result mutex
                resultDataMutex.lock();
                // push the finished work data
                resultData.push_back(data);
                // unlock
                resultDataMutex.unlock();
            }
            else
            {
                // there is no more work to do! all files have been scanned.
                abstractFilenamesMutex.unlock(); 
                // set the interrupt flag to kill the thread so that it can join.
                continueWorking = false;
            }
            
        } while(continueWorking);

    }
    catch(std::exception e)
    {
        // initialize a lock_guard, as the exception stack is a shared
        // resource.
        const std::lock_guard<std::mutex> exceptionStackLock(exceptionStackMutex);
        // if there is an exception, push it to the exception
        // stack so that it can be handled by the main thead.
        exceptionStack.push_back(e);
        // lock_guard out of scope
    }
}

// make a certain number of threads and make
// them begin working.
void makeThreads(unsigned int num)
{
    // store the thread objects in a vector so
    // that we can join them back to the main
    // thread properly. This is required in order
    // for the program to execute normally and 
    // terminate gracefully.
    std::vector<std::thread> threads;

    for(int i = 0; i < num; i++)
    {
        char threadName = 'A' + (char)i;
        threads.push_back(std::thread(threadLoop, std::string(1, threadName)));
    }

    for(std::thread& thread : threads)
        thread.join();

}

// takes an abstract file and generates a list of sentences that represent a summary.
// this is done by finding the sentences which share at least one word with the search
// query (Jaccane score > 0.0)
std::vector<std::string> makeSummary(const AbstractFileData& data)
{
    std::vector<std::string> summarySentences;

    for(std::string sentence : data.sentences)
    {
        if((*data.sentenceScores.find(sentence)).second > 0.0)
            summarySentences.push_back(sentence);
    }

    return summarySentences;
}

// send the final output to the logfile
// this involves the results from the scans
void finalOutput()
{
    // sort the work data in descending order of overall score
    std::sort(resultData.begin(), resultData.end(), [](const AbstractFileData& d1, const AbstractFileData& d2) {return d1.overallScore > d2.overallScore;});

    logLine("###");

    // fetch the best x abstracts, depending on how
    // many we were instructed to output
    for(int i = 0; i < numAbstractsToReturn; i++)
    {
        auto data = resultData[i];
        // output basic info
        logLine(std::string("Result ") + std::to_string(i+1) + std::string(":"));
        logLine(std::string("File: ") + data.name);
        // stringstream for fixed floating point precision output (4 places)
        std::stringstream ss;
        ss << "Score: " << std::fixed << std::setprecision(4) << data.overallScore;
        logLine(ss.str());
        // get the summary for the abstract and output it
        auto summary = makeSummary(data);
        std::string summaryString;
        for(std::string sentence : summary)
        {
            summaryString += (sentence + " ");
        }
        //summaryString = summaryString.substr(0, summaryString.length()-1);
        logLine(std::string("Summary: ") + summaryString);
        logLine("###");
    }

}

int main(int argc, char* argv[])
{

    // ##main program##

    if(!handleCommandlineArguments(argc, argv))
    {
        return -1;
    }
    
    if(!processInputFile(inputFilename))
    {
        return -1;
    }

    makeThreads(numThreads);
    finalOutput();

    return 0;
}
