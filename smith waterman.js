function smithWaterman(seq1, seq2, matchScore = 3, mismatchScore = -3, gapPenalty = -2) {
  const m = seq1.length + 1;
  const n = seq2.length + 1;
  const scoreMatrix = Array(m).fill().map(() => Array(n).fill(0));

  let maxScore = 0;
  let maxI = 0;
  let maxJ = 0;

  for (let i = 1; i < m; i++) {
    for (let j = 1; j < n; j++) {
      const match = scoreMatrix[i - 1][j - 1] + (seq1[i - 1] === seq2[j - 1] ? matchScore : mismatchScore);
      const deleteOp = scoreMatrix[i - 1][j] + gapPenalty;
      const insertOp = scoreMatrix[i][j - 1] + gapPenalty;
      scoreMatrix[i][j] = Math.max(0, match, deleteOp, insertOp);

      if (scoreMatrix[i][j] > maxScore) {
        maxScore = scoreMatrix[i][j];
        maxI = i;
        maxJ = j;
      }
    }
  }

  let alignedSeq1 = '';
  let alignedSeq2 = '';
  let i = maxI;
  let j = maxJ;
  while (scoreMatrix[i][j] > 0) {
    if (seq1[i - 1] === seq2[j - 1]) {
      alignedSeq1 = seq1[i - 1] + alignedSeq1;
      alignedSeq2 = seq2[j - 1] + alignedSeq2;
      i--;
      j--;
    } else if (scoreMatrix[i][j] === scoreMatrix[i - 1][j - 1] + mismatchScore) {
      alignedSeq1 = seq1[i - 1] + alignedSeq1;
      alignedSeq2 = seq2[j - 1] + alignedSeq2;
      i--;
      j--;
    } else if (scoreMatrix[i][j] === scoreMatrix[i - 1][j] + gapPenalty) {
      alignedSeq1 = seq1[i - 1] + alignedSeq1;
      alignedSeq2 = '-' + alignedSeq2;
      i--;
    } else {
      alignedSeq1 = '-' + alignedSeq1;
      alignedSeq2 = seq2[j - 1] + alignedSeq2;
      j--;
    }
  }

  return { alignedSeq1, alignedSeq2, score: maxScore };
}

// Example usage:
const seq1 = 'ATCG';
const seq2 = 'ACGT';
const result = smithWaterman(seq1, seq2);
console.log(result.alignedSeq1);
console.log(result.alignedSeq2);
console.log('Score:', result.score);
