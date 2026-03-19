class NoRoom(Exception):
    pass

class EmptyQueue(Exception):
    pass

class fsqueue:
    """
    A fixed-size dequeue has four attributes:
      - iArray: an internal array, containing the actual elements of the queues
        or dummy values (None)
      - the number of elements in the queue
      - the index where the first element of the queue is stored
      - the index of the next element to be enqueued
    """

    def __init__(self, n):
        self.iArray = [ None for i in range(0, n) ]
        self.size = 0
        # the next value is a bit bonkers for illustration
        # purposes; typically it would be set to 0, but I
        # made it more fun for illustration purposes.
        self.begin = n - 1 - n // 2
        self.end = self.begin

    # You need to modify this slightly for Task 7.1.a
    def enqueue(self, x):
        # Need to raise an exception when the queue is full
        n = len(self.iArray)

        if self.size >= n:
            raise NoRoom

        self.size += 1
        self.iArray[self.end] = x
        self.end = (self.end + 1) % n

    def __len__(self):
        return self.size

    # For you to do for Task 7.1.b
    # I don't understand why this takes an argument x
    def dequeue(self, x=None):
        if self.size <= 0:
            raise EmptyQueue
        
        n = len(self.iArray)

        self.size -= 1
        self.iArray[self.begin] = None
        self.begin = (self.begin + 1) % n

    # Utility function, no need to read
    def toList(self):
        if self.end < self.begin:
          return self.iArray[self.begin:] + self.iArray[:self.end]
        else:
          return self.iArray[self.begin:self.end]

    # Utility function to make the class fsqueue work with print
    def __str__(self):
        return '<< '  + ', '.join(map(lambda x: str(x),self.toList())) + ' >>'

# No need to read that next procedure, it's just for pretty printing
def strtable(t):
    nCol = max(map(len, t))
    def get(i,j):
        try:
            return str(t[i][j])
        except Exception:
            return ''
    wCol = [ max([len(get(i,j)) for i in range(0, len(t))]) for j in range(0,nCol)]
    line = '+' + '+'.join([ ''.join(['-'] * (i + 2)) for i in wCol ]) + '+\n'
    r = [line]
    for i in range(0, len(t)):
        r.append('| ' + ' | '.join([get(i, j) + ' ' * (wCol[j] - len(get(i,j))) for j in range(0, nCol)]) + ' |\n')
        r.append(line)
    return ''.join(r)

# A printing function 
def tellMeAboutThisQueue(q):
    print('The queue:', q, '\n')
    print('Internal stuff:')
    print(strtable([('iArray', q.iArray),
           ('begin', q.begin),
           ('end', q.end),
           ('size', q.size)
          ]))

if __name__ == "__main__":
    q = fsqueue(7)
    everyone = ['Glynn', 'Morgan', 'Rhys', 'Helen', 'Eleanor']
    for i in everyone:
        q.enqueue(i)
    q.enqueue('Anemone')
    # Task 7.1.a: what happens if you uncommend the next two lines
    q.enqueue('Trilobyte')
    q.dequeue()
    q.enqueue('Squid')
    q.dequeue()
    q.dequeue()
    q.dequeue()
    q.dequeue()
    q.dequeue()
    q.dequeue()
    q.dequeue()
    tellMeAboutThisQueue(q)
