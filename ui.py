import tkinter as tk
from search import stackoverflow_search

class SearchUI(tk.Frame):
  def __init__(self, master):
    super().__init__(master)

    self.query_entry = tk.Entry(self)
    self.query_entry.grid(row=0, column=0)

    self.search_button = tk.Button(self, text="Search", command=self.search)
    self.search_button.grid(row=0, column=1)

    # Create a frame to hold the table
    self.results_frame = tk.Frame(self)
    self.results_frame.grid(row=1, column=0, columnspan=2)

    # Create a label for each column in the table
    self.id_label = tk.Label(self.results_frame, text="ID")
    self.title_label = tk.Label(self.results_frame, text="Title")
    self.link_label = tk.Label(self.results_frame, text="Link")

    # Place the labels in the frame
    self.id_label.grid(row=0, column=0)
    self.title_label.grid(row=0, column=1)
    self.link_label.grid(row=0, column=2)

    # Create a list to store the rows in the table
    self.results_rows = []

  def search(self):
    query = self.query_entry.get()

    questions = stackoverflow_search(query)

    # Clear the table
    for row in self.results_rows:
      row.destroy()

    # Add each question to the table
    for question in questions:
      row = tk.Frame(self.results_frame)

      # Create a label for each column in the row
      id_label = tk.Label(row, text=question["id"])
      title_label = tk.Label(row, text=question["title"])
      link_label = tk.Label(row, text=question["link"])

      # Place the labels in the row
      id_label.grid(row=0, column=0)
      title_label.grid(row=0, column=1)
      link_label.grid(row=0, column=2)

      # Bind a hyperlink to the link label
      link_label.config(cursor="hand2")
      link_label.bind("<ButtonRelease-1>", lambda e: self.open_question(question["link"]))

      # Add the row to the table
      self.results_rows.append(row)

      # Grid the row
      row.grid(row=len(self.results_rows), column=0, columnspan=3)

  def open_question(self, url):
    import webbrowser
    webbrowser.open(url)

if __name__ == "__main__":
  root = tk.Tk()
  root.title("Stack Overflow Search")

  search_ui = SearchUI(root)
  search_ui.pack()

  root.mainloop()
