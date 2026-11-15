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

[Icons]
Name: "{commonprograms}\GW2 VLM COPILOT"; Filename: "{app}\GW2-VLM-COPILOT.exe"; WorkingDir: "{app}"

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

function SafeModelFolder: Boolean;
begin
  Result := (CompareText(ExpandConstant('{app}'),
    ExpandConstant('{autopf}\GW2-VLM-COPILOT')) = 0) and
    PlainDirectory(ExpandConstant('{autopf}')) and
    PlainDirectory(ExpandConstant('{app}')) and
    PlainDirectory(ExpandConstant('{app}\Models'));
end;

function ConfirmModelCleanup(Files: TStringList; TotalBytes: Int64): Boolean;
var
  Dialog: TSetupForm;
  Summary: TNewStaticText;
  Preview: TNewMemo;
  KeepButton, DeleteButton: TNewButton;
begin
  Dialog := CreateCustomForm(ScaleX(490), ScaleY(310), True, True);
  try
    Dialog.Caption := 'Optional model cleanup';
    Summary := TNewStaticText.Create(Dialog);
    Summary.Parent := Dialog;
    Summary.SetBounds(ScaleX(12), ScaleY(12), ScaleX(460), ScaleY(36));
    Summary.Caption := 'Models in the installed app folder' + #13#10 +
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
    KeepButton.Caption := 'Keep models';
    KeepButton.ModalResult := mrCancel;
    KeepButton.Default := True;
    KeepButton.Cancel := True;

    DeleteButton := TNewButton.Create(Dialog);
    DeleteButton.Parent := Dialog;
    DeleteButton.SetBounds(ScaleX(355), ScaleY(273), ScaleX(123), ScaleY(26));
    DeleteButton.Caption := 'Delete listed models';
    DeleteButton.ModalResult := mrYes;
    Dialog.ActiveControl := KeepButton;
    Result := Dialog.ShowModal = mrYes;
  finally
    Dialog.Free;
  end;
end;

procedure CurUninstallStepChanged(Step: TUninstallStep);
var
  Files: TStringList;
  Entry: TFindRec;
  Folder, Path: String;
  TotalBytes: Int64;
  Attributes: LongWord;
  Index, Failures: Integer;
begin
  if (Step <> usPostUninstall) or UninstallSilent or not SafeModelFolder then
    Exit;

  Folder := ExpandConstant('{app}\Models\');
  Files := TStringList.Create;
  try
    TotalBytes := 0;
    if FindFirst(Folder + '*.gguf', Entry) then
    try
      repeat
        if ((Entry.Attributes and (DirectoryAttribute or ReparseAttribute)) = 0) and
          (CompareText(ExtractFileExt(Entry.Name), '.gguf') = 0) then
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
    if not ConfirmModelCleanup(Files, TotalBytes) or not SafeModelFolder then
      Exit;

    Failures := 0;
    for Index := 0 to Files.Count - 1 do
    begin
      Path := Folder + Files[Index];
      Attributes := GetFileAttributes(Path);
      if SafeModelFolder and (Attributes <> MissingAttributes) and
        ((Attributes and (DirectoryAttribute or ReparseAttribute)) = 0) then
      begin
        if not DeleteFile(Path) then
          Failures := Failures + 1;
      end;
    end;
    RemoveDir(Folder);
    RemoveDir(ExpandConstant('{app}'));
    if Failures > 0 then
      MsgBox('Some selected models could not be deleted. Close any engine using them and check the Models folder.', mbInformation, MB_OK);
  finally
    Files.Free;
  end;
end;
