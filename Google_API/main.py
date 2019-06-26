try:
    from googlesearch import search
except ImportError:
    print("No Module named 'google' Found")

class Gsearch_python:
   def __init__(self,name_search):
      self.name = name_search
   def Gsearch(self):
      count = 0
      for i in search(query=self.name,stop=1,start=0):
         count += 1
         print (count)
         print(i + '\n')
if __name__=='__main__':
   gs = Gsearch_python("Tutorialspoint Python")
   gs.Gsearch()