const seqs = events.map(e => e.seq);            // 0,1,2,... liên tục
for (let i = 0; i < seqs.length; i++)
  if (seqs[i] !== i) gaps.push(i);             // lỗ hổng = mất một lần ghi
