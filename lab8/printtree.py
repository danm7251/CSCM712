class tree:
    def __init__(self, x, c = []):
        self.label = x
        self.children = []
        for i in c:
            self.children.append(i)

    def __str__(self):
        # h = '__'
        # d = '|'
        # f = '+'
        # t = 'L'
        # if your terminal support UTF8, you can uncomment the following lines
        # and get a prettier picture.
        t = '└'
        f = '├'
        d = '│'
        h = '──'
        """
        lh = len(h)
        r = ['a']
        r.append(f + h + ' b')
        r.append(d + ' ' * (lh + 1) + t + h + ' c')
        r.append(t + h + ' c')
        r.append(' ' + ' ' * (lh + 1) + f + h + ' d')
        r.append(' ' + ' ' * (lh + 1) + t + h + ' e')
        r.append(' ' + ' ' * (lh + 1) + ' ' + ' ' * lh + ' ' + t + h + ' f')
        return '\n'.join(r)"""

        count = lambda node: 1 + sum(count(c) for c in node.children)

        r = [self.label]
        for i, c in enumerate(self.children):
            if i >= len(self.children)-1:
                r.append(t)
            else:
                r.append(f)
            
        return '\n'.join(r)

if __name__ == "__main__":
  x = tree('a', [tree('b', [tree('c')]), tree('c', [tree('d'), tree('e', [tree('f')])])])
  print(x)
  y = tree('Desktop', [
        tree('Secret', [
            tree('secret.txt')
        ]),
        tree('Downloads', [
            tree('Tunic', [
                tree('Tunic.exe'),
                tree('verify.bat')
            ]),
            tree('Song.mp3')
        ])
    ])
print(y)