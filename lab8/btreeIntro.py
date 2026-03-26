class btree:
  def __init__(self, x, l = None, r = None):
        self.label = x
        self.left = l
        self.right = r

  def size(self):
        s = 1
        if self.left != None:
            s += size(self.left)
        if self.right != None:
            s += size(self.right)
        return s

  def depth(self):
      d = 1
      left = 0
      right = 0

      if self.left != None:
        left += self.left.depth()
      if self.right != None:
        right += self.right.depth()

      d += max(left, right)
      return d

  def insert(self, k):
    if self.label > k:
      if self.left != None:
        self.left.insert(k)
      else:
        self.left = btree(k)
    if self.label < k:
      if self.right != None:
        self.right.insert(k)
      else:
        self.right = btree(k)
      

  def prefixTraversal(self):
    res = [self.label]
    if self.left != None:
      res += self.left.prefixTraversal()
    if self.right != None:
      res += self.right.prefixTraversal()
    return res
      

  def __str__(self):
    res = '';
    if self.left != None:
      res += '(' + str(self.left) + ') '
    res += str(self.label)
    if self.right != None:
      res += ' (' + str(self.right) + ')'
    return res
  
  def __eq__(self, otherTree):
    if otherTree != None:
      label = self.label == otherTree.label
      left = self.left == otherTree.left
      right = self.right == otherTree.right

      if label and left and right:
        return True
     
    return False

  """
  toDot returns a string that generates a dot file that describes a graph
  representation of whatever the datastructure looks like (even if it is
  a bit nonsensical!)
  The representation format is the content of a would-be dot file that can
  be parsed by the tool graphviz.
  If you do not have graphviz on your computer (likely!), you may paste the output
  in e.g. https://dreampuf.github.io/GraphvizOnline or any similar tool. If you
  want to install graphviz, their official website is there: https://graphviz.org/
  WARNING: the picture will NOT differentiate between left and right nodes
  """
  @staticmethod #Similar to the static keyword in java
  def toDot(t):
    res = []
    res.append("digraph {\n")
    visited = []
    frontier = [t]
    def cellToString(n):
      if n == None:
        return "None"
      else:
        return str(n.label) + " (" + str(id(n)) + ")"
    def cellValToString(n):
      if n == None:
        return "None"
      else:
        return str(n.label)
    while len(frontier) != 0:
      cur = frontier.pop()
      visited.append(cur)
      successors = filter(lambda x: x[0] != None, [(cur.left, 'left'), (cur.right, 'right')])
      for suc in successors:
        res.append("  \"" + cellToString(cur) + "\" -> \"" + cellToString(suc[0]) + "\" [label = " + suc[1] + "];\n")
        if not suc[0] in visited:
          frontier.insert(0, suc[0])
    for n in visited:
      res.append("  \"" + cellToString(n) + "\" [label=\"" + cellValToString(n) + "\"];\n")
    res.append("}")
    return ''.join(res)

if __name__ == "__main__":
    example1 = btree(5, btree(-2, btree(15), btree(7)))
    example2 = btree(55, example1, btree(7, example1))
    print(btree.toDot(example1))
    example1.insert(4)
    print(btree.toDot(example1))

# 1b) Because despite having the same value x and y are different objects.
# I assume that to compare by value we would have to implement __eq__().