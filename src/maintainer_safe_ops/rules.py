from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    id: str
    severity: str
    message: str
    message_ja: str
    pattern: re.Pattern[str]
    help_uri: str


RULES: list[Rule] = [
    Rule(
        id="MSO001_OPENAI_KEY",
        severity="high",
        message="Possible OpenAI API key detected.",
        message_ja="OpenAI APIキーらしき文字列があります。",
        pattern=re.compile(r"\bsk-[A-Za-z0-9_\-]{20,}\b"),
        help_uri="https://platform.openai.com/docs",
    ),
    Rule(
        id="MSO002_SECRET_ASSIGNMENT",
        severity="high",
        message="Secret-looking assignment detected.",
        message_ja="秘密情報らしき代入があります。",
        pattern=re.compile(
            r"(?i)\b[\w-]*(api[_-]?key|secret|token|password|private[_-]?key)\b\s*[:=]\s*['\"]?[A-Za-z0-9_\-./+=]{8,}"
        ),
        help_uri="https://docs.github.com/code-security/secret-scanning",
    ),
    Rule(
        id="MSO003_SENSITIVE_ENV_NAME",
        severity="medium",
        message="Sensitive environment variable name detected.",
        message_ja="秘密情報に関連する環境変数名があります。",
        pattern=re.compile(
            r"(?i)\b(OPENAI_API_KEY|GITHUB_TOKEN|RAILWAY_TOKEN|DATABASE_URL|JWT_SECRET|AWS_SECRET_ACCESS_KEY|ANTHROPIC_API_KEY)\b"
        ),
        help_uri="https://docs.github.com/actions/security-guides/using-secrets-in-github-actions",
    ),
    Rule(
        id="MSO004_RM_RF_ROOT",
        severity="high",
        message="Dangerous root deletion command detected.",
        message_ja="危険な削除コマンド rm -rf / が含まれています。",
        pattern=re.compile(r"\brm\s+-rf\s+/(?:\s|$)"),
        help_uri="https://www.gnu.org/software/coreutils/manual/html_node/rm-invocation.html",
    ),
    Rule(
        id="MSO005_FORCE_PUSH",
        severity="medium",
        message="Force push command detected.",
        message_ja="force push コマンドが含まれています。",
        pattern=re.compile(r"\bgit\s+push\s+(?:--force|-f)\b"),
        help_uri="https://git-scm.com/docs/git-push",
    ),
    Rule(
        id="MSO006_PRODUCTION_DEPLOY",
        severity="medium",
        message="Production deployment wording detected.",
        message_ja="production deploy に関する記述があります。公開前に意図を確認してください。",
        pattern=re.compile(
            r"(?i)\b(production deploy|deploy production|prod deploy|railway up|vercel --prod)\b"
        ),
        help_uri="https://docs.github.com/actions/deployment",
    ),
    Rule(
        id="MSO007_PULL_REQUEST_TARGET_WRITE",
        severity="high",
        message="Potentially risky pull_request_target workflow with write permissions.",
        message_ja="pull_request_target と write 権限の組み合わせが疑われます。",
        pattern=re.compile(r"(?is)pull_request_target.*permissions:.*write"),
        help_uri="https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/",
    ),
    Rule(
        id="MSO008_ACTIONS_WRITE_ALL",
        severity="medium",
        message="GitHub Actions workflow grants broad write permissions.",
        message_ja="GitHub Actions workflowで広いwrite権限が設定されています。",
        pattern=re.compile(r"(?is)permissions:\s*write-all|contents:\s*write"),
        help_uri="https://docs.github.com/actions/security-guides/automatic-token-authentication",
    ),
    Rule(
        id="MSO009_CURL_PIPE_SHELL",
        severity="medium",
        message="Downloaded script piped directly into a shell (supply-chain risk).",
        message_ja="ダウンロードしたスクリプトを直接シェルへパイプしています（サプライチェーンのリスク）。",
        pattern=re.compile(r"(?i)\b(curl|wget)\b[^|\n]*\|\s*(sudo\s+)?(ba)?sh\b"),
        help_uri="https://www.cisa.gov/news-events/news/avoiding-social-engineering-and-phishing-attacks",
    ),
]
