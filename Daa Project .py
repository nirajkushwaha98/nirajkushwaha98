// ==============================================
// Movie Recommendation System (DAA Project)
// Language : C++
// Algorithm: Content-Based Filtering using Cosine Similarity
// ==============================================

#include <iostream>
#include <vector>
#include <string>
#include <map>
#include <cmath>
#include <sstream>
#include <algorithm>

using namespace std;

// ----------------------------------------------
// Function to split string into words
// ----------------------------------------------
vector<string> splitWords(string text) {
    vector<string> words;
    string word;
    stringstream ss(text);
    while (ss >> word) {
        words.push_back(word);
    }
    return words;
}

// ----------------------------------------------
// Function to compute cosine similarity
// ----------------------------------------------
double cosineSimilarity(vector<int>& A, vector<int>& B) {
    double dot = 0.0, magA = 0.0, magB = 0.0;
    for (size_t i = 0; i < A.size(); ++i) {
        dot += A[i] * B[i];
        magA += A[i] * A[i];
        magB += B[i] * B[i];
    }
    if (magA == 0 || magB == 0)
        return 0.0;
    return dot / (sqrt(magA) * sqrt(magB));
}

// ----------------------------------------------
// Main Program
// ----------------------------------------------
int main() {
    cout << "=====================================\n";
    cout << "   Movie Recommendation System\n";
    cout << "=====================================\n\n";

    // Step 1: Define movies and genres
    map<string, string> movies = {
        {"Avatar", "Action Adventure SciFi"},
        {"Titanic", "Romance Drama"},
        {"Jurassic World", "Action Adventure SciFi"},
        {"The Avengers", "Action SciFi"},
        {"The Dark Knight", "Action Crime Drama"},
        {"Inception", "Action SciFi Thriller"},
        {"Interstellar", "Adventure Drama SciFi"},
        {"Iron Man", "Action Adventure SciFi"},
        {"The Matrix", "Action SciFi"},
        {"Spider-Man", "Action Adventure Superhero"}
    };

    // Step 2: Collect all unique words (genres)
    vector<string> vocabulary;
    map<string, vector<string>> movieWords;

    for (auto& movie : movies) {
        vector<string> words = splitWords(movie.second);
        movieWords[movie.first] = words;
        for (string w : words) {
            if (find(vocabulary.begin(), vocabulary.end(), w) == vocabulary.end())
                vocabulary.push_back(w);
        }
    }

    // Step 3: Build feature vectors for each movie
    map<string, vector<int>> featureVectors;
    for (auto& movie : movieWords) {
        vector<int> vec(vocabulary.size(), 0);
        for (string w : movie.second) {
            for (size_t i = 0; i < vocabulary.size(); ++i) {
                if (vocabulary[i] == w) {
                    vec[i] = 1;
                }
            }
        }
        featureVectors[movie.first] = vec;
    }

    // Step 4: Take input from user
    string inputMovie;
    cout << "Enter a movie name: ";
    getline(cin, inputMovie);

    if (movies.find(inputMovie) == movies.end()) {
        cout << "\nMovie not found in database.\n";
        return 0;
    }

    // Step 5: Compute similarity with all other movies
    vector<pair<string, double>> similarities;
    for (auto& movie : movies) {
        if (movie.first != inputMovie) {
            double sim = cosineSimilarity(featureVectors[inputMovie], featureVectors[movie.first]);
            similarities.push_back(make_pair(movie.first, sim));
        }
    }

    // Step 6: Sort by similarity (descending)
    sort(similarities.begin(), similarities.end(),
         [](pair<string, double>& a, pair<string, double>& b) {
             return a.second > b.second;
         });

    // Step 7: Display top 5 recommendations
    cout << "\nRecommended Movies similar to '" << inputMovie << "':\n";
    cout << "---------------------------------------------\n";
    int count = 0;
    for (auto& pair : similarities) {
        if (count >= 5) break;
        cout << "🎥 " << pair.first << "  (Similarity: " << pair.second << ")\n";
        count++;
    }

    cout << "\n=====================================\n";
    cout << "     End of Recommendation\n";
    cout << "=====================================\n";

    return 0;
}
