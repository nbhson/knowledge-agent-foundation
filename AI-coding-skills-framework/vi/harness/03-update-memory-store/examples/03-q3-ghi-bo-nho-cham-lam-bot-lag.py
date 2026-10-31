self.cache[key] = entry                      # ghi tức thì
self.pending_writes.append(entry)            # xếp hàng xả nền
if len(self.pending_writes) >= 100: self._flush()
# ack chỉ sau khi ghi nhật ký WAL + kho chính
