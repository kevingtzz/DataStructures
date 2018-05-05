#!/usr/bin/python
#ABB implementation

class TreeNode:
    def __init__(self,key ,value, Lson = None, Rson = None, father=None):
        self.key = key
        self.value = value
        self.Lson = Lson
        self.Rson = Rson
        self.father = father

    def hasLson(self):
        return self.Lson

    def hasRson(self):
        return self.Rson

    def isLson(self):
        return self.father and self.father.Lson == self

    def isRson(self):
        return self.father and self.father.Rson == self

    def isRoot(self):
        return not self.father

    def isLeaf(self):
        return not (self.Rson or self.Lson)

    def hasAnySon(self):
        return self.Rson or self.Lson

    def hasBothSon(self):
        return self.Rson and self.Lson

    def replaceNodeData(self,key,value,Lson,Rson):
        self.key = key
        self.value = value
        self.Lson = Lson
        self.Rson = Rson
        if self.hasLson():
            self.Lson.father = self
        if self.hasRson():
            self.Rson.father = self


class BinarySearchTree:

    def __init__(self):
        self.raiz = None
        self.size = 0

    def length(self):
        return self.size

    def __len__(self):
        return self.size

    def add(self,key,value):
        if self.raiz:
            self._add(key,value,self.raiz)
        else:
            self.raiz = TreeNode(key,value)
        self.size = self.size + 1

    def _add(self,key,value,currentNode):
        if key < currentNode.key:
            if currentNode.hasLson():
                   self._add(key,value,currentNode.Lson)
            else:
                   currentNode.Lson = TreeNode(key,value,father = currentNode)
        else:
            if currentNode.hasRson():
                   self._add(key,value,currentNode.Rson)
            else:
                   currentNode.Rson = TreeNode(key,value,father = currentNode)

    def __setitem__(self,key,value):
       self.add(key,value)

    def get(self,key):
       if self.raiz:
           result = self._get(key,self.raiz)
           if result:
                  return result.value
           else:
                  return None
       else:
           return None

    def _get(self,key,currentNode):
       if not currentNode:
           return None
       elif currentNode.key == key:
           return currentNode
       elif key < currentNode.key:
           return self._get(key,currentNode.Lson)
       else:
           return self._get(key,currentNode.Rson)

    def __getitem__(self,key):
       return self.get(key)

    def __contains__(self,key):
       if self._get(key,self.raiz):
           return True
       else:
           return False

    def delete(self,key):
      if self.size > 1:
         nodeToDelete = self._get(key,self.raiz)
         if nodeToDelete:
             self.remove(nodeToDelete)
             self.size = self.size-1
         else:
             raise KeyError('Error, key is not in the tree')
      elif self.size == 1 and self.raiz.key == key:
         self.raiz = None
         self.size = self.size - 1
      else:
         raise KeyError('Error, key is not in the tree')

    def __delitem__(self,key):
       self.delete(key)

    def splice(self):
       if self.isLeaf():
           if self.isLson():
                  self.father.Lson = None
           else:
                  self.father.Rson = None
       elif self.hasAnySon():
           if self.hasLson():
                  if self.isLson():
                     self.father.Lson = self.Lson
                  else:
                     self.father.Rson = self.Lson
                  self.Lson.father = self.father
           else:
                  if self.isLson():
                     self.father.Lson = self.Rson
                  else:
                     self.father.Rson = self.Rson
                  self.Rson.father = self.father

    def findSuccessor(self):
      successor = None
      if self.hasRson():
          successor = self.Rson.findMin()
      else:
          if self.father:
                 if self.isLson():
                     successor = self.father
                 else:
                     self.father.Rson = None
                     successor = self.father.findSuccessor()
                     self.father.Rson = self
      return successor

    def findMin(self):
      current = self
      while current.hasLson():
          current = current.Lson
      return current

    def remove(self,currentNode):
         if currentNode.isLeaf(): #hoja
           if currentNode == currentNode.father.Lson:
               currentNode.father.Lson = None
           else:
               currentNode.father.Rson = None
         elif currentNode.hasBothSon(): #interior
           successor = currentNode.findSuccessor()
           successor.splice()
           currentNode.key = successor.key
           currentNode.value = successor.value

         else: # este nodo has un (1) hijo
           if currentNode.hasLson():
             if currentNode.isLson():
                 currentNode.Lson.father = currentNode.father
                 currentNode.father.Lson = currentNode.Lson
             elif currentNode.isRson():
                 currentNode.Lson.father = currentNode.father
                 currentNode.father.Rson = currentNode.Lson
             else:
                 currentNode.replaceNodeData(currentNode.Lson.key,
                                    currentNode.Lson.value,
                                    currentNode.Lson.Lson,
                                    currentNode.Lson.Rson)
           else:
             if currentNode.isLson():
                 currentNode.Rson.father = currentNode.father
                 currentNode.father.Lson = currentNode.Rson
             elif currentNode.isRson():
                 currentNode.Rson.father = currentNode.father
                 currentNode.father.Rson = currentNode.Rson
             else:
                 currentNode.replaceNodeData(currentNode.Rson.key,
                                    currentNode.Rson.value,
                                    currentNode.Rson.Lson,
                                    currentNode.Rson.Rson)
