on run argv
  set outText to ""
  tell application "Microsoft Excel"
    set wb to active workbook
    repeat with nm in argv
      set sh to worksheet (nm as text) of wb
      set vals to value of range "A1:EZ50" of sh
      set outText to outText & "@@SHEET@@" & nm & "@@ROW@@"
      set AppleScript's text item delimiters to "@@C@@"
      repeat with rw in vals
        set outText to outText & (rw as text) & "@@ROW@@"
      end repeat
      set AppleScript's text item delimiters to ""
    end repeat
  end tell
  return outText
end run
