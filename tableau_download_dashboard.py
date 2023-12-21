from tableauserverclient import Server, ConnectionCredentials
from version import VERSION
import tableauserverclient as TSC

# Tableau Server information
tableau_server_url = "http://SampleServer.com/"
api_version = VERSION  # Choose the appropriate API version
view_id = "" # Need to identify view name first, see find_workbook_and_view_id.py
username = ""
password = ""
download_folder = "C:\\Users\\user\\Downloads"

# Sign in to Tableau Server
tableau_auth = TSC.TableauAuth(username, password)
server = TSC.Server(tableau_server_url)
server.version = api_version
server.use_server_version()


with server.auth.sign_in(tableau_auth):
    # Get the view
    view = server.views.get_by_id(view_id)

    # Download PDF
    pdf_path = f"{download_folder}\\VIEW_NAME.pdf"
    server.views.populate_pdf(view)
    with open(pdf_path, "wb") as pdf_file:
        pdf_file.write(view.pdf)

print(f"PDF downloaded successfully to {pdf_path}")
