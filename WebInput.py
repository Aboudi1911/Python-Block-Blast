import webbrowser
#FR13, EU1: Generate HTML table and open it in the browser
def viewWeb(recordArray):
    #Open an HTML file for writing
    with open("table.html", "w") as fileout:
        #Write the basic HTML structure with the table
        fileout.write("""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Highscores</title>
            <style>
                html {
                    height:100%;
                    background-image: linear-gradient(#00665E, #008F83);
                }    
                h1 {
                    text-align: center;
                    font-size: 50px;
                    font-family: Impact, Haettenschweiler, "Franklin Gothic", Charcoal,
                    "Helvetica Inserat", "Bitstream Vera Sans", "Arial Black", sans-serif;
                    color: #80a4ed;
                }
                table {
                    border-collapse: collapse;
                    width: 20%;
                    margin: auto;
                }
                th, td {
                    border: 1px solid black;
                    padding: 8px;
                    text-align: center;
                    color: #80a4ed;
                }
                th {
                    background-color: #f2f2f2;
                }
            </style>
        </head>
        <body>
            <header>
                <center>
                    <h1>Highscores</h1>
                </center>
            </header>
            <table>
        """)

        #Add the rows of the 2D array to the table
        for score in recordArray:
            if score.user != None:
                fileout.write("<tr>")
                fileout.write(f"<td>{score.user}</td>")
                fileout.write(f"<td>{score.score}</td>")
                fileout.write("</tr>")
        
        #Close the HTML structure
        fileout.write("""
            </table>
        </body>
        </html>
        """)
    
    #Open the HTML file in the default web browser
    webbrowser.open("table.html", new=2, autoraise=True)
