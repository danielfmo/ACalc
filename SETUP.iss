#define MyAppName "ACalc"
#define MyAppServerName "ACalc Server"
#define MyAppPublisher "Daniel Oliveira"
#define MyAppExeName "ACalc.exe"
#define MyConfigName "Settings"
#define MyConfigExeName "server.ini"
#define MyAppURL "http://localhost:8080/"

[Setup]
AppID={code:GetAppID|''}
AppName={#MyAppName}
AppVersion={code:GetAppVersion|''}
AppVerName={#MyAppName} {code:GetAppVersion|''} build {code:GetAppBuild|''}
AppPublisher={#MyAppPublisher}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=SETUP
OutputBaseFilename={#MyAppName}-setup
Compression=lzma
SolidCompression=yes
UsePreviousLanguage=no

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; 

[Files]
Source: "C:\Acalc_Server\build\exe.win32-3.3\ACalc.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Acalc_Server\build\exe.win32-3.3\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "version.dat"; DestDir: "{tmp}"; Flags: dontcopy
Source: "build.dat"; DestDir: "{tmp}"; Flags: dontcopy

[Icons]
Name: "{group}\{#MyAppServerName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{#MyAppServerName}"; Filename: "{app}\{#MyAppURL}"
Name: "{group}\{#MyConfigName}"; Filename: "{app}\conf\{#MyConfigExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppServerName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{commondesktop}\{#MyConfigName}"; Filename: "{app}\conf\{#MyConfigExeName}"; Tasks: desktopicon
Name: "{commondesktop}\{#MyAppName}"; Filename: "{#MyAppURL}"; Tasks: desktopicon

;[Run]
;Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent unchecked

[UninstallDelete]
Type: files; Name: "{app}\{#MyAppExeName}"

[Registry]
Root: HKLM; Subkey: Software\{#MyAppName}; ValueType: string; ValueName: Version; ValueData: {code:GetAppVersion|''}; Flags: uninsdeletekey 
Root: HKLM; Subkey: Software\{#MyAppName}; ValueType: string; ValueName: Build; ValueData: {code:GetAppBuild|''}; Flags: uninsdeletekey

[Code]
function GetAppID(param: String): String;
	begin
		Result := 'ACalc';
	end;
	
function GetAppVersion(param: String): String;
	var
		AppVersion: String;
	begin
		ExtractTemporaryFile('version.dat');
		LoadStringFromFile(ExpandConstant('{tmp}\version.dat'), AppVersion);
		Result := AppVersion;
	end;
	
function GetAppBuild(param: String): String;
	var
		BuildVersion: String;
	begin
		ExtractTemporaryFile('build.dat');
		LoadStringFromFile(ExpandConstant('{tmp}\build.dat'), BuildVersion);
		Result := BuildVersion;
	end;
