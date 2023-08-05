// //////////////////////////////////////////////////////////////////////
// Import section
// //////////////////////////////////////////////////////////////////////
// STL
#include <string>
#include <vector>
// OpenTREP
#include <opentrep/bom/Levenshtein.hpp>

namespace OPENTREP {

  // //////////////////////////////////////////////////////////////////
  int Levenshtein::getDistance (const std::string& iSource,
                                const std::string& iTarget) {

    // Step 1

    const int n = iSource.length();
    const int m = iTarget.length();
    
    if (n == 0) {
      return m;
    }
    
    if (m == 0) {
      return n;
    }

    // Definition of Matrix Type
    typedef std::vector<std::vector<int> > Matrix_T; 

    Matrix_T matrix (n+1);

    // Size the vectors in the 2.nd dimension. Unfortunately C++ doesn't
    // allow for allocation on declaration of 2.nd dimension of vec of vec

    for (int i = 0; i <= n; i++) {
      matrix[i].resize(m+1);
    }

    // Step 2

    for (int i = 0; i <= n; i++) {
      matrix[i][0]=i;
    }

    for (int j = 0; j <= m; j++) {
      matrix[0][j]=j;
    }

    // Step 3

    for (int i = 1; i <= n; i++) {

      const char s_i = iSource[i-1];

      // Step 4

      for (int j = 1; j <= m; j++) {

        const char t_j = iTarget[j-1];

        // Step 5

        int cost;
        if (s_i == t_j) {
          cost = 0;
          
        } else {
          cost = 1;
        }

        // Step 6

        const int above = matrix[i-1][j];
        const int left = matrix[i][j-1];
        const int diag = matrix[i-1][j-1];
        int cell = std::min ( above + 1, std::min (left + 1, diag + cost));

        // Step 6A: Cover transposition, in addition to deletion,
        // insertion and substitution. This step is taken from:
        // Berghel, Hal ; Roach, David : "An Extension of Ukkonen's 
        // Enhanced Dynamic Programming ASM Algorithm"
        // (http://www.acm.org/~hlb/publications/asm/asm.html)

        if (i>2 && j>2) {
          int trans = matrix[i-2][j-2] + 1;

          if (iSource[i-2] != t_j) {
            trans++;
          }
          
          if (s_i != iTarget[j-2]) {
            trans++;
          }
          
          if (cell > trans) {
            cell = trans;
          }
        }

        matrix[i][j] = cell;
      }
    }

    // Step 7

    return matrix[n][m];
  }

}
