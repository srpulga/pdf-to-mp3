; Inno Setup Script para Conversor de Midia MP3
; Compilar com: iscc installer.iss

#define MyAppName "Conversor MP3"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Conversor MP3"
#define MyAppURL "https://github.com/seu-usuario/pdf-to-mp3"
#define MyAppExeName "ConversorMP3.exe"

[Setup]
AppId={{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; Output
OutputDir=..\..\installers\output
OutputBaseFilename=ConversorMP3_Setup_{#MyAppVersion}
; Visual
SetupIconFile=..\..\assets\icon.ico
WizardStyle=modern
; Compression
Compression=lzma2/ultra64
SolidCompression=yes
; Permissions
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog
; Misc
DisableProgramGroupPage=yes
LicenseFile=..\..\LICENSE
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "portuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Copiar toda a pasta do PyInstaller output
Source: "..\..\dist\ConversorMP3\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; IconFilename: "{app}\{#MyAppExeName}"
Name: "{group}\Desinstalar {#MyAppName}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Iniciar {#MyAppName}"; Flags: nowait postinstall skipifsilent

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
