import tkinter


class SampleApp(tkinter.Tk):
    def __init__(self, *args, **kwargs):
        tkinter.Tk.__init__(self, *args, **kwargs) # Initialize tkinter.
        
        # Display a window when the program starts.
        self.title("Welcome")
        
        self.next_screen_button = tkinter.Button(self, command = self.show_next_screen,
                                                 text = "Show Next Screen")
        self.next_screen_button.pack()

    def show_next_screen(self):
        self.withdraw() 
        self.toplevel_for_scrollbar = tkinter.Toplevel(self)
        self.toplevel_for_scrollbar.title("Here is a scrollbar")
        self.label_text = ("The scrollbar should be below here")
        self.label = tkinter.Label(self.toplevel_for_scrollbar, text = self.label_text)
        self.label.pack()

        # Scrollbars in tkinter are complicated.  Here is the procedure:
        # (1) Create a Canvas (parent is toplevel).
        # (2) Create a scrollbar (parent is toplevel, NOT Canvas).  Make
        #     sure that the Scrollbar's command and the Canvas's
        #     xscrollcommand know about each other.    
        # (3) Create a Frame with the Canvas as parent.  Use
        #     Canvas.create_window (instead of pack or grid) to add the
        #     Frame.
        # (4) Place whatever needs to be displayed in the Frame.
        # (5) After calling update(), set the Canvas's scrollregion.
        # (6) Use Scrollbar.pack() to place the Scrollbar.

        # Step 1
        self.canvas_for_data = tkinter.Canvas(self.toplevel_for_scrollbar)
        self.canvas_for_data.pack(fill = "x", expand = True)
        # Step 2
        self.data_preview_scrollbar = tkinter.Scrollbar(self.toplevel_for_scrollbar,
                                                        command=self.canvas_for_data.xview,
                                                        orient=tkinter.HORIZONTAL)
        self.canvas_for_data.configure(xscrollcommand = self.data_preview_scrollbar.set)
        # Step 3
        self.frame_for_data = tkinter.Frame(self.canvas_for_data)
        self.canvas_for_data.create_window(0, 0, window=self.frame_for_data, anchor = 'nw')
        # Step 4
        for i in range(10):
            for j in range(10):
                tkinter.Label(self.frame_for_data,text = "(row, col) = (%d, %d)" %(j, i)).grid(row = j, column = i)    
         # Step 5
        self.update()
        self.canvas_for_data.config(scrollregion = self.canvas_for_data.bbox(tkinter.ALL))
        # Step 6
        self.data_preview_scrollbar.pack(side = tkinter.BOTTOM, fill = tkinter.X)


app = SampleApp()
app.mainloop()
