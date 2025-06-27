function needlemanWunsch(seq1, seq2, matchScore = 1, mismatchScore = -1, gapPenalty = -1) {
  const m = seq1.length + 1;
  const n = seq2.length + 1;
  const scoreMatrix = Array(m).fill().map(() => Array(n).fill(0));

  // Initialize score matrix
  for (let i = 0; i < m; i++) {
    scoreMatrix[i][0] = gapPenalty * i;
  }
  for (let j = 0; j < n; j++) {
    scoreMatrix[0][j] = gapPenalty * j;
  }

  // Fill score matrix
  for (let i = 1; i < m; i++) {
    for (let j = 1; j < n; j++) {
      const match = scoreMatrix[i - 1][j - 1] + (seq1[i - 1] === seq2[j - 1] ? matchScore : mismatchScore);
      const deleteOp = scoreMatrix[i - 1][j] + gapPenalty;
      const insertOp = scoreMatrix[i][j - 1] + gapPenalty;
      scoreMatrix[i][j] = Math.max(match, deleteOp, insertOp);
    }
  }

  // Trace back aligned sequences
  let alignedSeq1 = '';
  let alignedSeq2 = '';
  let i = m - 1;
  let j = n - 1;
  while (i > 0 && j > 0) {
    const score = scoreMatrix[i][j];
    const match = scoreMatrix[i - 1][j - 1] + (seq1[i - 1] === seq2[j - 1] ? matchScore : mismatchScore);
    const deleteOp = scoreMatrix[i - 1][j] + gapPenalty;
    const insertOp = scoreMatrix[i][j - 1] + gapPenalty;

    if (score === match) {
      alignedSeq1 = seq1[i - 1] + alignedSeq1;
      alignedSeq2 = seq2[j - 1] + alignedSeq2;
      i--;
      j--;
    } else if (score === deleteOp) {
      alignedSeq1 = seq1[i - 1] + alignedSeq1;
      alignedSeq2 = '-' + alignedSeq2;
      i--;
    } else {
      alignedSeq1 = '-' + alignedSeq1;
      alignedSeq2 = seq2[j - 1] + alignedSeq2;
      j--;
    }
  }

  while (i > 0) {
    alignedSeq1 = seq1[i - 1] + alignedSeq1;
    alignedSeq2 = '-' + alignedSeq2;
    i--;
  }

  while (j > 0) {
    alignedSeq1 = '-' + alignedSeq1;
    alignedSeq2 = seq2[j - 1] + alignedSeq2;
    j--;
  }

  return { alignedSeq1, alignedSeq2, score: scoreMatrix[m - 1][n - 1] };
}

// Example usage:
const seq1 = 'ATCG';
const seq2 = 'ACGT';
const result = needlemanWunsch(seq1, seq2);
console.log(result.alignedSeq1);
console.log(result.alignedSeq2);
console.log('Score:', result.score);
