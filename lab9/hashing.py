"""
  This file plays the roles of both "lecture notes" for lecture 9 and template
  for lab 9. Most of the comments are written with lab 9 in mind :)
"""

from copy import copy

# No need to understand that next procedure (until line 61),
# it's just for pretty printing
def strtable(t):
    nCol = max(map(len, t))
    h = '-'
    x = '+'
    tt = '+'
    lt = '+'
    ur = '+'
    ul = '+'
    lr = '+'
    ll = '+'
    xl = '+'
    xr = '+'
    # comment out/delete the next 10 lines if your terminal can't deal with UTF8
    h = '━'
    x = '╋'
    tt = '┳'
    lt = '┻'
    ul = '┏'
    ur = '┓'
    lr = '┛'
    ll = '┗'
    v = '┃'
    xl = '┣'
    xr = '┫'
    def get(i,j):
        try:
            return str(t[i][j])
        except Exception:
            return ''
    def intersperse(d, xs):
        if len(xs) <= 1:
            return copy(xs)
        r = []
        for i in range(0, len(xs) - 1):
          r.append(xs[i])
          r.append(d)
        r.append(xs[-1])
        return r

    wCol = [ max([len(get(i,j)) for i in range(0, len(t))]) for j in range(0,nCol)]
    topline = ul + tt.join([ ''.join([h] * (i + 2)) for i in wCol ]) + ur
    midline = xl + x.join([ ''.join([h] * (i + 2)) for i in wCol ]) + xr
    botline = ll + lt.join([ ''.join([h] * (i + 2)) for i in wCol ]) + lr
    ilines = [ v + ' ' +\
               (' ' + v + ' ').join(\
                 [' ' * ((wCol[j] - len(get(i,j))) // 2) +\
                  get(i, j) +\
                  ' ' * (wCol[j] - len(get(i,j)) - (wCol[j] - len(get(i,j))) // 2)\
                  for j in range(0, nCol)]\
               ) + ' ' + v
              for i in range(0, len(t))]
    return '\n'.join([topline] + intersperse(midline,ilines) + [botline])


# An implementation without collision resolution (Bad!)
class hopelessHashTable:

  def __init__(self, capacity = 50):
     self.table = [ None for _ in range(0, 2 * capacity)]
  
  def __getitem__(self, key):
     return self.table[hash(key) % len(self.table)]
  
  def __setitem__(self, key, value):
     self.table[hash(key) % len(self.table)] = (key, value)
  
  def __contains__(self, key):
      return self.table[hash(key) % len(self.table)] != None 

  def __str__(self):
      n = len(self.table)
      idxs = ['idx'] + list(range(0, n))
      keys = ['key']
      vals = ['val']
      for c in self.table:
         if c == None:
             keys.append('')
             vals.append('')
         else:
             keys.append(c[0])
             vals.append(c[1])
      return strtable([idxs, keys, vals])

  def delitem(self, key):
      self.table[hash(key) % len(self.table)] = None

# Traditionally, chained hash tables use linked lists, in lieu of the
# sets I am using here, but the idea is the same
# The code is relatively simple, so I will let you figure out how it works by
# reading
class chainingHashTable:

  def __init__(self, capacity = 50):
     self.table = [ set() for _ in range(0, 2 * capacity)]
     self.occupancy = 0

  def __getitem__(self, key):
     for (k, v) in self.table[hash(key) % len(self.table)]:
       if k == key:
         return v
     raise KeyError(k)

  def __setitem__(self, key, value):
     n = len(self.table)
     # the next two branches deal with resizing the hash table if it looks
     # to small or big, before proceeding with the actual algorithm
     # of setting the value
     if n * 0.75 < self.occupancy:
            print('bla')
            self.resize(n * 2)
            n *= 2
     elif n / 20 > self.occupancy + 2:
            self.resize(n // 2)
            n = n // 2
     n = len(self.table)
     bucket = self.table[hash(key) % n]
     for i in bucket:
       if i[0] == key:
         bucket.remove(i)
         self.occupancy -= 1
     bucket.add((key, value))
     self.occupancy += 1

  def __contains__(self, key):
      for (k, _) in self.table[hash(key) % len(self.table)]:
        if k == key:
          return True
      return False

  # For you to do in Lab 9! Please write a few tests to check that this method
  # works correctly
  def delitem(self, key):
      bucket = self.table[hash(key) % len(self.table)]

      target = None

      # Use target variable to not change set during iteration
      for item in bucket:
          if item[0] == key:
              target = item
              break

      if target != None:
          bucket.remove(target)
          self.occupancy -= 1
      else:
          raise KeyError
        

  # Create a bigger table, and copy over the dictionary encoded by the old
  # table. Note that one needs to rehash the elements as len(self.table)
  # changes
  def resize(self, n):
      oldTable = self.table
      self.table = [ True for _ in range(0, n * 2)]
      for z in oldTable:
        if not (z in [True, False]):
            (x, y) = z
            self[x] = y


  # for pretty-printing; no need to understand what's going on there
  def __str__(self):
      r = [['idx', '(key, value) pairs']]
      for i in range(0, len(self.table)):
          if len(self.table[i]) == 0:
              c = ''
          else:
              c = str(self.table[i])[1:-1]
          r.append([i, c])
      return strtable(r)

if __name__ == "__main__":
    c = chainingHashTable(4)

    def testDeletingStuff(x):
            print('Deleting ', x)
            
            if x in c:
                print('Key found in bucket:', hash(x) % len(c.table))
                c.delitem(x)
                print('Successfully removed ', x)
            else:
                print('Key ', x, ' not found, delitem should raise error')
                try:
                    c.delitem(x)
                except KeyError:
                    print('Caught KeyError.')
            
            print('Internal table after deletion:')
            print(c)
            print('Current occupancy:', c.occupancy)

    c["Hello"] = 53
    c["Snakes"] = "Zebras"

    testDeletingStuff("Hello")
    testDeletingStuff("Mr Bean")

"""
Hash tables with probing and resizing

By default will use linear probing, but you can change that by changing the
value of the attribute probeNext which is the rehashing function: it takes
as inputs the length of the array containing the table and the hash to be
rehashed.

To set a custom probing strategy, pass it as the second argument to the constructor.
It is supposed to be a function of two arguments that take as input the
length of the hash table and the index to be rehashed (yes you can pass functions
as arguments).

Otherwise, the attributes table and occupancy should typically not messed with
outside of the method of the class.
"""
class probingHashtable:
    """
    Initializing a hash table
    The main attribute is self.table, which is an array; each cell contains
    three type of cells:
    * if set to True, it means the cell is unoccupied and was never occupied
      before. Hence, any search that ends up looking there should be terminated
    * if set to False, it means the cell is unoccupied, but was occupied in
      the past. It means that it is free to get filled, but any search that
      ends up there should not be terminated
    * otherwise it contains a single (key, value) pair
    """
    def __init__(self, capacity = 10, probingFun = lambda n , i: (i + 1) % n, c = []):
        self.table = [ True for _ in range(0, max(len(c), capacity) * 2)]
        self.probeNext = probingFun
        self.occupancy = 0
        for (k, v) in c:
           self[k] = v

    # How to read a cell
    def __getitem__(self, k):
        n = len(self.table)
        # hash to compute the initial index
        i = hash(k) % n
        # while we have not found a spot that was never occupied
        while self.table[i] != True:
            # if the key matches, return the corresponding value
            if self.table[i] != False and self.table[i][0] == k:
                return self.table[i][1]
            # otherwise, look at the next spot
            i = self.probeNext(n,i)
        # if we are out of the look, the key simply did not exist in the table
        raise IndexError

    # Create a bigger table, and copy over the dictionary encoded by the old
    # table. Note that one needs to rehash the elements as len(self.table)
    # changes
    def resize(self, n):
        oldTable = self.table
        self.table = [ True for _ in range(0, n * 2)]
        self.occupancy = 0
        for z in oldTable:
          if not (z in [True, False]):
              (x, y) = z
              self[x] = y

    def __len__(self):
        return self.occupancy

    def __setitem__(self, k, v):
        n = len(self.table)
        # the next two branches deal with resizing the hash table if it looks
        # to small or big, before proceeding with the actual algorithm
        # of setting the value
        if n * 0.75 < self.occupancy:
            print('bla')
            self.resize(n * 2)
            n *= 2
        elif n / 20 > self.occupancy + 2:
            self.resize(n // 2)
            n = n // 2
        # compute the index
        i = hash(k) % len(self.table)
        # while the we are not on a free spot...
        while not (self.table[i] in [True, False]):
           # if the key match, replace the old value and terminate
           if self.table[i][0] == k:
               self.table[i] = (k, v)
               return
           # otherwise rehash to the next spot
           i = self.probeNext(n, i)
        # we have found a free spot! set it, and raise the occupancy count
        self.table[i] = (k, v)
        self.occupancy += 1

    def __contains__(self, k):
        n = len(self.table)
        i = hash(k) % n
        while self.table[i] != True:
            if self.table[i] != False and self.table[i][0] == k:
                return True
            i = self.probeNext(n,i)
        return False

    # TODO for you: you should complete the code for this method, and then
    # write tests below to show it off working.
    # The tombstone should be appearing in the tests you write. To make your
    # tests deterministic, you may use integer keys.
    def delitem(self, k):
        i = hash(k) % len(self.table)
        # Look until first pristine spot
        while self.table[i] != True:
            # If not a tombstone
            if self.table[i] != False:   
                # if the key match
                if self.table[i][0] == k:
                    self.table[i] = False
                    self.occupancy -= 1
                    return
                
            i = self.probeNext(len(self.table), i)

        raise KeyError(k)
    
    # for pretty-printing; no need to understand what's going here
    def __str__(self):
      ded = '#'
      ded = '_⊓_' # comment out this line if your terminal can't deal with UTF8
      n = len(self.table)
      idxs = ['idx'] + list(range(0, n))
      hashs = ['hash']
      keys = ['key']
      vals = ['val']
      for c in self.table:
         if c == True:
             hashs.append(' ')
             keys.append(' ')
             vals.append(' ')
         elif c == False:
             hashs.append(' ')
             keys.append(ded)
             vals.append(' ')
         else:
             hashs.append(hash(c[0]) % n)
             keys.append(c[0])
             vals.append(c[1])
      return strtable([idxs, hashs, keys, vals])



"""
  Here begins the code executed when you run the script!
  After getting an understanding of what it does and dealing with the lab
  tasks, you need to modify this to test out the delitem methods.
"""

if __name__ == "__main__":
    c = chainingHashTable(4)

    def testDeletingStuffc(x):
            print('Deleting ', x)
            
            if x in c:
                print('Key found in bucket:', hash(x) % len(c.table))
                c.delitem(x)
                print('Successfully removed ', x)
            else:
                print('Key ', x, ' not found, delitem should raise error')
                try:
                    c.delitem(x)
                except KeyError:
                    print('Caught KeyError.')
            
            print('Internal table after deletion:')
            print(c)
            print('Current occupancy:', c.occupancy)

    c["Hello"] = 53
    c["Snakes"] = "Zebras"

    testDeletingStuffc("Hello")
    testDeletingStuffc("Mr Bean")

    h = probingHashtable(4)
    def testAddingstuff(x, y):
        print('Adding', x, 'with hash', hash(x))
        print('Note:', hash(x), 'mod', len(h.table), '=', hash(x) % len(h.table))
        h[x] = y
        print('The internal table is:')
        print(h)
    for (x, y) in {('gull', 785), ('swan', 54), ('magpie', 21), ('dove', 55)}:
        testAddingstuff(x, y)

    def testDeletingStuffh(x):
            print('Deleting ', x)
            
            if x in h:
                print('Key found in:', hash(x) % len(h.table))
                h.delitem(x)
                print('Successfully removed ', x)
            else:
                print('Key ', x, ' not found, delitem should raise error')
                try:
                    h.delitem(x)
                except KeyError:
                    print('Caught KeyError.')
            
            print('Internal table after deletion:')
            print(h)
            print('Current occupancy:', h.occupancy)

    testDeletingStuffh('swan')
