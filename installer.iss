  ; ==============================================
; Instalador YT-DLP Automation - Script Inno Setup
; ==============================================

[Setup]
AppName=YT-DLP Automation
AppVersion=1.0
AppPublisher=Seu Nome ou Empresa
DefaultDirName={autopf}\YT-DLP Automation
DefaultGroupName=YT-DLP Automation
OutputDir=dist
OutputBaseFilename=YT-DLP-Installer
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=admin

SetupIconFile=icon.ico
WizardSmallImageFile=logo.bmp

LicenseFile=license.txt

MinVersion=6.1.7600
; Windows 7 ou superior

UninstallDisplayIcon={app}\yt-dlp_gui.exe
Uninstallable=yes

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: desktopicon; Description: "Criar atalho na Área de Trabalho"; GroupDescription: "Opções adicionais:"; Flags: unchecked

[Files]
Source: "dist\yt-dlp_gui.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "icon.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "license.txt"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\YT-DLP Downloader GUI"; Filename: "{app}\yt-dlp_gui.exe"; IconFilename: "{app}\icon.ico"
Name: "{userdesktop}\YT-DLP Downloader GUI"; Filename: "{app}\yt-dlp_gui.exe"; Tasks: desktopicon; IconFilename: "{app}\icon.ico"

[Run]
Filename: "{app}\yt-dlp_gui.exe"; Description: "Executar YT-DLP Automation"; Flags: nowait postinstall skipifsilent

[Code]

function IsDotNet45Installed(): Boolean;
var
  Release: Cardinal;
  Success: Boolean;
begin
  Success := RegQueryDWordValue(HKLM, 'SOFTWARE\Microsoft\NET Framework Setup\NDP\v4\Full', 'Release', Release);
  if Success then
    Result := Release >= 378389
  else
    Result := False;
end;

function IsPythonInstalled(): Boolean;
var
  ResultCode: Integer;
begin
  // Executa 'python --version' no cmd e verifica se executou com sucesso
  Result := Exec('cmd.exe', '/c python --version', '', SW_HIDE, ewWaitUntilTerminated, ResultCode) and (ResultCode = 0);
end;

procedure InitializeWizard();
begin
  // Verifica se o Python está instalado
  if not IsPythonInstalled() then
  begin
    MsgBox('O Python não foi encontrado neste sistema. Este aplicativo requer o Python instalado para funcionar corretamente. Baixe em https://www.python.org', mbError, MB_OK);
    WizardForm.Close;
    Exit;
  end;

  // Verifica se .NET Framework 4.5 ou superior está instalado
  if not IsDotNet45Installed() then
  begin
    MsgBox('.NET Framework 4.5 ou superior não encontrado. Por favor, instale o .NET Framework antes de continuar.', mbError, MB_OK);
    WizardForm.Close;
    Exit;
  end;
end;
