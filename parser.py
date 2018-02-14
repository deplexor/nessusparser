from shutil import copyfile
from appJar import gui
import sqlite3
import xml2sql as x
conn = sqlite3.connect('reports.db')

def import_options(button):
	if button == "ok1":
		x.xml2sqlite(app.getEntry("File"))
		print("Successfully converted %s to sqlite database" % app.getEntry("File"))
		app.removeAllWidgets()
		start_gui()
	else:
		exit()

def select_options(button):
	if button == "ok2":
		cb_list = [cb for cb in app.getAllCheckBoxes() if app.getCheckBox(cb)]
		for cb in cb_list:
			c = conn.cursor()
			c.execute("select reports.host_ip from reportitems INNER JOIN reports ON reports.report_id = reportitems.report_id WHERE reportitems.plugin_name LIKE 'Unencrypted Telnet Server' AND reports.report_name = ?", [cb])
			all_rows = c.fetchall()
			if len(all_rows) > 0:
				copyfile('plugins/telnet-services.txt', './' + cb + '.txt')
				with open('./' + cb + '.txt', "a") as t_file:
					[ t_file.write(str(append_line[0] + '\n')) for append_line in all_rows ]
		print("Done")
		exit()
	else:
		exit()

app = gui("NessusParser", "335x235")
def start_gui():
	app.startTabbedFrame("TabbedFrame")
	app.startTab("Import")
	app.addLabel("file_dest", "Click to open file")
	app.addFileEntry("File")
	row = app.getRow()
	app.addNamedButton("OK", "ok1", import_options, row, 1)
	app.addNamedButton("Exit", "exit1", import_options, row, 2)
	app.stopTab()

	app.startTab("Select")
	try:
		c = conn.cursor()
		c.execute('select DISTINCT reports.report_name from reports')
		for rc in c.fetchall():
			app.addCheckBox(rc[0])
	except sqlite3.OperationalError:
		app.addLabel('The database appears to be empty.\nImport a file first')
	
	row = app.getRow()
	app.addNamedButton("OK", "ok2", select_options, row, 1)
	app.addNamedButton("Exit", "exit2", select_options, row, 2)
	app.stopTab()
	app.stopTabbedFrame()

start_gui()
app.go()
