' http://serverfault.com/questions/29707/download-file-from-vbscript

url = "http://peak.telecommunity.com/dist/ez_setup.py"
file = "ez_setup.py"

Set objXMLHTTP = CreateObject("MSXML2.XMLHTTP")

objXMLHTTP.open "GET", url, false
objXMLHTTP.send()

If objXMLHTTP.Status = 200 Then
  Set objADOStream = CreateObject("ADODB.Stream")
  objADOStream.Open
  objADOStream.Type = 1 'adTypeBinary

  objADOStream.Write objXMLHTTP.ResponseBody
  objADOStream.Position = 0    'Set the stream position to the start

  Set objFSO = Createobject("Scripting.FileSystemObject")
    If objFSO.Fileexists(file) Then objFSO.DeleteFile file
  Set objFSO = Nothing

  objADOStream.SaveToFile file
  objADOStream.Close
  Set objADOStream = Nothing
End if

Set objXMLHTTP = Nothing