[Setup]
AppId=GW2-VLM-COPILOT
AppName=GW2 VLM COPILOT
AppVersion={#AppVersion}
DefaultDirName={autopf}\GW2-VLM-COPILOT
DisableDirPage=yes
PrivilegesRequired=admin
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
SetupIconFile={#Payload}\assets\branding\gw2-vlm-copilot.ico
UninstallDisplayIcon={app}\GW2-VLM-COPILOT.exe
CloseApplications=yes
RestartApplications=no

[Files]
Source: "{#Payload}\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Dirs]
Name: "{app}\Models"
Name: "{app}\runtime"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; Flags: unchecked

[Icons]
Name: "{commonprograms}\GW2 VLM COPILOT"; Filename: "{app}\GW2-VLM-COPILOT.exe"; WorkingDir: "{app}"
Name: "{commondesktop}\GW2 VLM COPILOT"; Filename: "{app}\GW2-VLM-COPILOT.exe"; WorkingDir: "{app}"; Tasks: desktopicon

[Run]
Filename: "{app}\GW2-VLM-COPILOT.exe"; Parameters: "--setup"; WorkingDir: "{app}"; Description: "Open resource setup (download server, NVIDIA DLLs, and models)"; Flags: postinstall nowait skipifsilent runasoriginaluser

[Code]
const
  DirectoryAttribute = $10;
  ReparseAttribute = $400;
  MissingAttributes = $FFFFFFFF;

function GetFileAttributes(Path: String): LongWord;
  external 'GetFileAttributesW@kernel32.dll stdcall';

function PlainDirectory(Path: String): Boolean;
var
  Attributes: LongWord;
begin
  Attributes := GetFileAttributes(Path);
  Result := (Attributes <> MissingAttributes) and
    ((Attributes and (DirectoryAttribute or ReparseAttribute)) = DirectoryAttribute);
end;

function SafeCleanupFolder(Folder: String): Boolean;
var
  UserData: String;
begin
  Result := False;
  if CompareText(ExpandConstant('{app}'), ExpandConstant('{autopf}\GW2-VLM-COPILOT')) <> 0 then
    Exit;
  if (CompareText(Folder, ExpandConstant('{app}\Models')) = 0) or
     (CompareText(Folder, ExpandConstant('{app}\runtime')) = 0) then
    Result := PlainDirectory(ExpandConstant('{autopf}')) and
      PlainDirectory(ExpandConstant('{app}')) and PlainDirectory(Folder);
  UserData := ExpandConstant('{localappdata}\GW2 VLM COPILOT');
  if CompareText(Folder, UserData + '\Models') = 0 then
    Result := PlainDirectory(ExpandConstant('{localappdata}')) and
      PlainDirectory(UserData) and PlainDirectory(Folder);
  if CompareText(Folder, UserData + '\runtime\llama-b12387') = 0 then
    Result := PlainDirectory(ExpandConstant('{localappdata}')) and
      PlainDirectory(UserData) and PlainDirectory(UserData + '\runtime') and PlainDirectory(Folder);
end;

function ConfirmCleanup(Files: TStringList; TotalBytes: Int64; Folder, ItemLabel: String): Boolean;
var
  Dialog: TSetupForm;
  Summary: TNewStaticText;
  Preview: TNewMemo;
  KeepButton, DeleteButton: TNewButton;
begin
  Dialog := CreateCustomForm(ScaleX(490), ScaleY(310), True, True);
  try
    Dialog.Caption := 'Optional cleanup';
    Summary := TNewStaticText.Create(Dialog);
    Summary.Parent := Dialog;
    Summary.SetBounds(ScaleX(12), ScaleY(12), ScaleX(460), ScaleY(36));
    Summary.Caption := Folder + #13#10 +
      'Total file size: ' + IntToStr(TotalBytes div 1048576) + ' MiB';

    Preview := TNewMemo.Create(Dialog);
    Preview.Parent := Dialog;
    Preview.SetBounds(ScaleX(12), ScaleY(54), ScaleX(466), ScaleY(204));
    Preview.ReadOnly := True;
    Preview.ScrollBars := ssVertical;
    Preview.Lines.Assign(Files);

    KeepButton := TNewButton.Create(Dialog);
    KeepButton.Parent := Dialog;
    KeepButton.SetBounds(ScaleX(225), ScaleY(273), ScaleX(120), ScaleY(26));
    KeepButton.Caption := 'Keep ' + ItemLabel;
    KeepButton.ModalResult := mrCancel;
    KeepButton.Default := True;
    KeepButton.Cancel := True;

    DeleteButton := TNewButton.Create(Dialog);
    DeleteButton.Parent := Dialog;
    DeleteButton.SetBounds(ScaleX(355), ScaleY(273), ScaleX(123), ScaleY(26));
    DeleteButton.Caption := 'Delete listed files';
    DeleteButton.ModalResult := mrYes;
    Dialog.ActiveControl := KeepButton;
    Result := Dialog.ShowModal = mrYes;
  finally
    Dialog.Free;
  end;
end;

function CleanupFileMatches(Name: String; IsRuntime: Boolean): Boolean;
var
  Extension: String;
begin
  Extension := Lowercase(ExtractFileExt(Name));
  if IsRuntime then
    Result := (Extension = '.dll') or
      ((Extension = '.exe') and (Pos('llama-', Lowercase(Name)) = 1))
  else
    Result := Extension = '.gguf';
end;

procedure OfferCleanup(Folder, ItemLabel: String; IsRuntime: Boolean);
var
  Files: TStringList;
  Entry: TFindRec;
  Path: String;
  TotalBytes: Int64;
  Attributes: LongWord;
  Index, Failures: Integer;
begin
  if not SafeCleanupFolder(Folder) then
    Exit;

  Files := TStringList.Create;
  try
    TotalBytes := 0;
    if FindFirst(AddBackslash(Folder) + '*', Entry) then
    try
      repeat
        if ((Entry.Attributes and (DirectoryAttribute or ReparseAttribute)) = 0) and
          CleanupFileMatches(Entry.Name, IsRuntime) then
        begin
          Files.Add(Entry.Name);
          TotalBytes := TotalBytes + (Int64(Entry.SizeHigh) shl 32) + Entry.SizeLow;
        end;
      until not FindNext(Entry);
    finally
      FindClose(Entry);
    end;

    if Files.Count = 0 then
      Exit;
    if not ConfirmCleanup(Files, TotalBytes, Folder, ItemLabel) or not SafeCleanupFolder(Folder) then
      Exit;

    Failures := 0;
    for Index := 0 to Files.Count - 1 do
    begin
      Path := AddBackslash(Folder) + Files[Index];
      Attributes := GetFileAttributes(Path);
      if SafeCleanupFolder(Folder) and (Attributes <> MissingAttributes) and
        ((Attributes and (DirectoryAttribute or ReparseAttribute)) = 0) then
      begin
        if not DeleteFile(Path) then
          Failures := Failures + 1;
      end;
    end;
    RemoveDir(Folder);
    RemoveDir(ExpandConstant('{app}'));
    if Failures > 0 then
      MsgBox('Some listed files could not be deleted. Close any engine using them and check ' + Folder + '.', mbInformation, MB_OK);
  finally
    Files.Free;
  end;
end;

procedure CurUninstallStepChanged(Step: TUninstallStep);
begin
  if (Step <> usPostUninstall) or UninstallSilent then
    Exit;
  OfferCleanup(ExpandConstant('{app}\Models'), 'models', False);
  OfferCleanup(ExpandConstant('{app}\runtime'), 'runtime', True);
  OfferCleanup(ExpandConstant('{localappdata}\GW2 VLM COPILOT\Models'), 'models', False);
  OfferCleanup(ExpandConstant('{localappdata}\GW2 VLM COPILOT\runtime\llama-b12387'), 'runtime', True);
end;
