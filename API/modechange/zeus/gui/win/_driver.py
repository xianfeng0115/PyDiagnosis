
import _element

class WinDriver(_element.TypedElement):
    def __init__(self):              
        self.__app = None        
        self.root = _element.root()
        
    @property
    def main(self):
        try:
            return self.root.Window(pid = self.__app.pid)
        except:
            return self.root.Element(pid = self.__app.pid)
    
    def open(self, path, timeout=0, args = ''):
        import subprocess, time
        path = '%s %s' % (path, args)
        self.__app = subprocess.Popen(path)
        time.sleep(timeout)
        
    def find(self, **kwargs):
        return self.main.find(**kwargs)
    
    def find_all(self, **kwargs):
        return self.main.find_all(**kwargs)
    
    def close(self):        
        self.main.close()
    
    def quit(self):
        if self.__app:
            return self.__app.kill()
    
#    def Pane(self, **criteria):
#        return self.main.Pane(**criteria)
#    
#    def Window(self, **criteria):
#        return self.main.Window(**criteria)
#    
#    def Button(self, **criteria):
#        return self.main.Button(**criteria)
#    
#    def Edit(self, **criteria):
#        return self.main.Edit(**criteria)
#    
#    def Text(self, **criteria):
#        return self.main.Text(**criteria)
#    
#    def ProcessBar(self, **criteria):
#        return self.main.ProcessBar(**criteria)
#    
#    def Menu(self, **criteria):
#        return self.main.Menu(**criteria)
#    
#    def MenuItem(self, **criteria):
#        return self.main.MenuItem(**criteria)
#    
#    def List(self, **criteria):
#        return self.main.List(**criteria)
#    
#    def ListItem(self, **criteria):
#        return self.main.ListItem(**criteria)
#    
#    def TitleBar(self, **criteria):
#        return self.main.TitleBar(**criteria)
#    
#    def ToolBar(self, **criteria):
#        return self.main.ToolBar(**criteria)
#    
#    def Tooltip(self, **criteria):
#        return self.main.Tooltip(**criteria)
#    
#    def CheckBox(self, **criteria):
#        return self.main.CheckBox(**criteria)
#    
#    def ComboBox(self, **criteria):
#        return self.main.ComboBox(**criteria)
#    
#    def Hyperlink(self, **criteria):
#        return self.main.Hyperlink(**criteria)
#    
#    def Image(self, **criteria):
#        return self.main.Image(**criteria)
#    
#    def RadioButton(self, **criteria):
#        return self.main.RadioButton(**criteria)
#    
#    def Tree(self, **criteria):
#        return self.main.Tree(**criteria)
#    
#    def TreeItem(self, **criteria):
#        return self.main.TreeItem(**criteria)
#    
#    def Slider(self, **criteria):
#        return self.main.Slider(**criteria)
#    
#    def Grid(self, **criteria):
#        return self.main.Grid(**criteria)
#    
#    def GridItem(self, **criteria):
#        return self.main.GridItem(**criteria)
#    
#    def Group(self, **criteria):
#        return self.main.Group(**criteria)
#    
#    def MenuBar(self, **criteria):
#        return self.main.MenuBar(**criteria)
#    
#    def Spinner(self, **criteria):
#        return self.main.Spinner(**criteria)
#    
#    def SplitButton(self, **criteria):
#        return self.main.SplitButton(**criteria)
#    
#    def ScrollBar(self, **criteria):
#        return self.main.ScrollBar(**criteria)
#    
#    def StatusBar(self, **criteria):
#        return self.main.StatusBar(**criteria)
#    
#    def Tab(self, **criteria):
#        return self.main.Tab(**criteria)
#    
#    def TabItem(self, **criteria):
#        return self.main.TabItem(**criteria)
#    
#    def Table(self, **criteria):
#        return self.main.Table(**criteria)
#    
#    def Thumb(self, **criteria):
#        return self.main.Thumb(**criteria)
        

