import json
from openai import OpenAI
from app.config import MIMO_API_KEY, MIMO_BASE_URL, MIMO_MODEL
from app.models.schemas import ResumeInfo, MatchResult

client = OpenAI(api_key=MIMO_API_KEY, base_url=MIMO_BASE_URL)


def _call_mimo(system_msg: str, prompt: str) -> str:
    response = client.chat.completions.create(
        model=MIMO_MODEL,
        messages=[
            {"role": "system", "content": system_msg},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=8192,
    )
    return response.choices[0].message.content


def _parse_json(text: str) -> dict:
    text = text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()
    return json.loads(text)


def _call_mimo_json(system_msg: str, prompt: str, default: dict) -> dict:
    try:
        return _parse_json(_call_mimo(system_msg, prompt))
    except json.JSONDecodeError:
        return default


def extract_resume_info(resume_text: str) -> dict:
    prompt = f"""从以下简历文本中提取信息，返回JSON。注意：所有字段必须从原文原样提取，禁止改写、总结、省略。

字段：
- name: 姓名
- phone: 电话号码
- email: 邮箱地址
- address: 地址
- job_intention: 求职意向（原文内容）
- expected_salary: 期望薪资（原文内容）
- work_years: 工作年限（原文内容）
- education: 学历背景（原文内容）
- project_experience: 项目经历——必须将简历中所有项目经历的完整原文复制到这里，包括每个项目的名称、技术栈、时间段、项目描述、职责描述等所有细节，一字不改。绝对不要只写项目名称或做任何摘要。

找不到的字段设为null。

简历原文：
{resume_text}

只返回JSON，不要其他文字。"""

    return _call_mimo_json(
        "你是简历信息提取助手，严格按要求提取信息，不省略不改写。",
        prompt,
        ResumeInfo().model_dump(),
    )


def match_resume_to_job(resume_info: dict, resume_text: str, job_description: str) -> dict:
    prompt = f"""你是一个专业的招聘匹配分析师。请将以下简历信息与岗位需求进行匹配分析。

岗位需求：
{job_description}

简历信息：
{json.dumps(resume_info, ensure_ascii=False)}

简历原文摘要：
{resume_text[:2000]}

请以JSON格式返回分析结果，包含以下字段：
- match_score: 整体匹配度评分（0-100的整数）
- skill_match_rate: 技能匹配率（0-100的整数）
- experience_relevance: 工作经验相关性（0-100的整数）
- analysis: 详细的文字分析说明（200字以内）

请只返回JSON格式的结果，不要包含其他文字。"""

    return _call_mimo_json(
        "你是招聘匹配分析师，客观分析岗位与简历的匹配度。",
        prompt,
        MatchResult(match_score=0, skill_match_rate=0, experience_relevance=0, analysis="分析失败").model_dump(),
    )
