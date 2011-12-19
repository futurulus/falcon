import wx
import schedule

class FlightsPanel(wx.Panel):
    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        
        self.MainSizer = wx.BoxSizer(wx.VERTICAL)
        
        self.AddPanel = AddPanel(parent=self)
        self.MainSizer.Add(self.AddPanel, border=4, proportion=0,
                flag=wx.EXPAND | wx.ALL)
        
        self.FlightsList = FlightsList(parent=self)
        self.MainSizer.Add(self.FlightsList, border=4, proportion=1,
                flag=wx.EXPAND | wx.LEFT | wx.RIGHT | wx.BOTTOM)
        
        self.SetAutoLayout(True)
        self.SetSizer(self.MainSizer)
        self.Layout()
        
        self.Bind(wx.EVT_SIZE, self.OnSize)
    
    def OnSize(self, e):
        self.SetSize(e.GetSize())
        self.Layout()
    
    def AddFlight(self, entry):
        self.FlightsList.AddFlight(entry)

class FlightsList(wx.HtmlListBox):
    INITIAL_LENGTH = 100

    def __init__(self, *args, **kwargs):
        wx.HtmlListBox.__init__(self, *args, **kwargs)
        self.schedule = schedule.Schedule()
        self.Refresh()
        
    def OnGetItem(self, n):
        return self.Format(self.schedule.get(n))
        
    def Format(self, entry):
        return entry.report(self.schedule)

    def Refresh(self):
        self.SetItemCount(self.schedule.num_flights(first=
                FlightsList.INITIAL_LENGTH))
        self.RefreshAll()

    def AddFlight(self, entry):
        self.schedule.add(entry)
        self.Refresh()

class AddPanel(wx.TextCtrl): # TODO: change to true panel
    def __init__(self, *args, **kwargs):
        wx.TextCtrl.__init__(self, style=wx.TE_PROCESS_ENTER, *args, **kwargs)
        self.Bind(wx.EVT_TEXT_ENTER, self.OnEnter)
    
    def OnEnter(self, e):
        try:
            self.GetParent().AddFlight(self.GetValue())
        except ValueError, e:
            self.ErrorMessageBox(e.message)

    def ErrorMessageBox(self, message):
        dialog = wx.MessageDialog(self, message, 'Error adding flight',
                                  wx.OK | wx.ICON_ERROR)
        dialog.ShowModal()
        dialog.Destroy()
