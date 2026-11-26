<#
.SYNOPSIS
  Install seo-strategist-growth-engine for Claude Code, OpenAI Codex, Google Antigravity, or Cursor.
#>
param(
  [Parameter(Mandatory = $true)]
  [ValidateSet("claude", "codex", "antigravity", "cursor")]
  [string]$Target,

  [ValidateSet("project", "global")]
  [string]$Scope = "project",

  [string]$ProjectDir = (Get-Location).Path,

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

$Dest = Join-Path $DestBase "seo-strategist-growth-engine"
Write-Host "Source:      $SkillSrc"
Write-Host "Destination: $Dest"

if ($DryRun) {
  Write-Host "[Dry Run] Would install seo-strategist-growth-engine into $Dest"
  exit 0
}

New-Item -ItemType Directory -Force -Path $Dest | Out-Null
foreach ($item in @("SKILL.md", "README.md", "references", "templates", "scripts", "integrations", "examples")) {
  $srcPath = Join-Path $SkillSrc $item
  $dstPath = Join-Path $Dest $item
  if (Test-Path $srcPath) {
    if (Test-Path $dstPath) {
      Remove-Item -Recurse -Force $dstPath
    }
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

$SharedPolicy = Join-Path (Split-Path $SkillSrc -Parent) "Context-Optimizer-Skill\agent-token-efficiency\references\default-policy.md"
if (Test-Path $SharedPolicy) {
  $PolicyDestDir = Join-Path $DestBase "agent-token-efficiency\references"
  New-Item -ItemType Directory -Force -Path $PolicyDestDir | Out-Null
  Copy-Item -Force $SharedPolicy (Join-Path $PolicyDestDir "default-policy.md")
}

Write-Host "Installed seo-strategist-growth-engine to $Dest"
