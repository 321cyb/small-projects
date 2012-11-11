#include <iostream>
#include <string>

#include <ctime>
#include <cstdlib>
#include <cctype>

using namespace std;

//https://gist.github.com/4019515, here's Chen shuo's answer.


//Do exactly the same as random.shuffle.
void random_shuffle(string &word)
{
    for(int i = word.length() - 1; i > 0; i--)
    {
        int j = random() % (i + 1);
        char temp = word[i];
        word[i] = word[j];
        word[j] = temp;
    }
}

string process_a_word(const string &word)
{
    string ret("");
    if(word.size() > 3)
    {
        string middle = word.substr(1, word.size() - 2);
        random_shuffle(middle);
        ret = word[0]+ middle + word[word.size()-1];
    }
    else
    {
        ret = word;
    }
    return ret;
}

string typoglycemia(string & src)
{
    string segment("");
    string ret("");

    srand(time(NULL));

    for(string::iterator ps = src.begin(); ps != src.end(); ps++)
    {
        if(! isalpha(*ps) )
        {
            ret += process_a_word(segment);
            ret += *ps;
            segment = "";
        }
        else
        {
            segment += *ps;
        }
    }

    return ret;
}

int main(int argc, char *argv[])
{
    string text("According to a research at Cambridge University, it doesn't matter in what order the letters in a word are, the only important thing is that the first and last letter be at the right place, the reset can be a total mess and you can still read it without problem. This is because the human mind does not read every letter by itself, but the word as a whole. Amazing!");

    string result = typoglycemia(text);
    cout << result << endl;

    return 0;
}
