param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("claude", "codex", "antigravity", "cursor")]
  [string]$Target,

  [ValidateSet("project", "global")]
  [string]$Scope = "project",

  [string]$ProjectDir = (Get-Location).Path,

  [switch]$PolicyOnly,

  [switch]$DryRun
)

$ErrorActionPreference = "Stop"
$SkillSrc = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

$DestBase = switch ("$Target`:$Scope") {
  "claude:project"      { Join-Path $ProjectDir ".claude\skills" }
  "claude:global"       { Join-Path $HOME ".claude\skills" }
  "codex:project"       { Join-Path $ProjectDir ".agents\skills" }
  "codex:global"        { Join-Path $HOME ".codex\skills" }
  "antigravity:project" { Join-Path $ProjectDir ".agents\skills" }
  "antigravity:global"  { Join-Path $HOME ".gemini\config\skills" }
  "cursor:project"      { Join-Path $ProjectDir ".cursor\skills" }
  "cursor:global"       { Join-Path $HOME ".cursor\skills" }
  default               { throw "Unsupported target/scope: $Target`:$Scope" }
}

$Dest = Join-Path $DestBase "agent-token-efficiency"
if ($DryRun) {
  Write-Host "[Dry Run] Would install to $Dest (PolicyOnly=$PolicyOnly)"
  exit 0
}

if ($PolicyOnly) {
  $refDst = Join-Path $Dest "references"
  New-Item -ItemType Directory -Force -Path $refDst | Out-Null
  Copy-Item -Force (Join-Path $SkillSrc "references\default-policy.md") (Join-Path $refDst "default-policy.md")
} else {
  New-Item -ItemType Directory -Force -Path $Dest | Out-Null
  foreach ($item in @("SKILL.md", "README.md", "references", "templates", "scripts", "examples")) {
    $srcPath = Join-Path $SkillSrc $item
    $dstPath = Join-Path $Dest $item
    if (Test-Path $srcPath) {
      if (Test-Path $dstPath) { Remove-Item -Recurse -Force $dstPath }
      Copy-Item -Recurse -Force $srcPath $dstPath
    }
  }
  if ($Target -eq "codex") {
    $openaiSrc = Join-Path $SkillSrc "adapters\codex\agents\openai.yaml"
    if (Test-Path $openaiSrc) {
      $agentsDir = Join-Path $Dest "agents"
      New-Item -ItemType Directory -Force -Path $agentsDir | Out-Null
      Copy-Item -Force $openaiSrc (Join-Path $agentsDir "openai.yaml")
    }
  }
}

Write-Host "Installed agent-token-efficiency to $Dest"
