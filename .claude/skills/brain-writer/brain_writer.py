#!/usr/bin/env python3
"""
Brain Writer — Reference Implementation

Core writing tool for the Brain Protocol. Handles frontmatter, naming
conventions, and automatic index updates for wiki/, diary/, and todo/.

This is a minimal reference implementation. Platforms may extend it with
additional features (entity linking, image management, external drivers, etc.).

Public API:
    create_entity(entity_type, name, content, tags)  -> Path
    create_log(date, title, content, tags, project)  -> Path
    create_diary(date, content, tags, title)          -> Path
    create_todo(date, title, content, tags, priority, due, project) -> Path
    update_file(file_path, content, frontmatter_updates, append) -> Path
    get_frontmatter(file_path) -> dict

Usage:
    from brain_writer import create_log, create_entity, update_file

    create_log('2026-04-28', 'deploy-fix', 'Fixed nginx config', 
               tags=['deploy'], project='my-project')

    create_entity('people', 'John Doe', 'CTO at Acme Corp',
                  tags=['contact', 'acme'])
"""

from datetime import datetime
from pathlib import Path
import yaml
import re
import subprocess


# Brain root = git repo root
def _brain_root():
    try:
        return Path(subprocess.check_output(
            ['git', 'rev-parse', '--show-toplevel'],
            cwd=Path(__file__).parent, text=True, stderr=subprocess.DEVNULL
        ).strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback: walk up until we find boot/brain.md
        p = Path(__file__).parent
        while p != p.parent:
            if (p / 'boot' / 'brain.md').exists():
                return p
            p = p.parent
        return Path.cwd()

BRAIN_ROOT = _brain_root()


def _sanitize(name):
    """Convert any string to a valid filename slug."""
    name = name.lower().strip()
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    name = re.sub(r'[\s_]+', '-', name)
    name = re.sub(r'-+', '-', name).strip('-')
    return name


def _build_frontmatter(data):
    """Build YAML frontmatter string from dict."""
    # Filter None values
    data = {k: v for k, v in data.items() if v is not None}
    return '---\n' + yaml.dump(data, default_flow_style=False, allow_unicode=True).strip() + '\n---\n'


def _write_file(file_path, content):
    """Write content to file, creating parent directories."""
    path = Path(file_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding='utf-8')
    _update_folder_index(path)
    return path


def _update_folder_index(file_path):
    """Update the folder's index.yaml with the new file entry."""
    folder = Path(file_path).parent
    index_path = folder / 'index.yaml'
    
    if not index_path.exists():
        return
    
    try:
        with open(index_path) as f:
            index = yaml.safe_load(f) or {}
    except yaml.YAMLError:
        return
    
    entries = index.get('entries', [])
    filename = Path(file_path).name
    
    # Don't duplicate
    if any(e.get('file') == filename for e in entries):
        return
    
    # Extract title from frontmatter or filename
    fm = get_frontmatter(file_path)
    title = fm.get('title', filename.replace('.md', '').replace('-', ' ').title())
    
    entries.append({
        'file': filename,
        'title': title,
        'date': datetime.now().strftime('%Y-%m-%d')
    })
    
    index['entries'] = entries
    index['updated'] = datetime.now().strftime('%Y-%m-%d')
    
    with open(index_path, 'w') as f:
        yaml.dump(index, f, default_flow_style=False, allow_unicode=True)


def _extract_wiki_links(content):
    """Find [[wiki-links]] in content and return them."""
    return re.findall(r'\[\[([^\]|]+)(?:\|([^\]]+))?\]\]', content or '')


def get_frontmatter(file_path):
    """Read and parse YAML frontmatter from a file."""
    path = Path(file_path)
    if not path.exists():
        return {}
    
    text = path.read_text(encoding='utf-8')
    match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not match:
        return {}
    
    try:
        return yaml.safe_load(match.group(1)) or {}
    except yaml.YAMLError:
        return {}


def create_entity(entity_type, name, content='', tags=None, metadata=None):
    """
    Create a wiki entity (person, company, project, tech, etc.).
    
    Args:
        entity_type: Folder name in wiki/ (people, companies, projects, tech, skills)
        name: Entity name (will be slugified for filename)
        content: Markdown body
        tags: List of tags
        metadata: Extra frontmatter fields
    
    Returns:
        Path to created file
    """
    slug = _sanitize(name)
    tags = list(tags or [])
    if entity_type not in [t.strip() for t in (tags or [])]:
        tags.insert(0, entity_type.rstrip('s') if entity_type.endswith('s') else entity_type)
    
    now = datetime.now()
    fm_data = {
        'type': entity_type.rstrip('s') if entity_type.endswith('s') else entity_type,
        'created': now.strftime('%Y-%m-%d'),
        'created_at': now.strftime('%Y-%m-%d %H:%M:%S'),
        'created_with': 'brain-writer',
        'tags': tags,
    }
    if metadata:
        fm_data.update(metadata)
    
    # Projects get a folder with index.md, others get a flat file
    if entity_type == 'projects':
        file_path = BRAIN_ROOT / 'wiki' / entity_type / slug / 'index.md'
    else:
        file_path = BRAIN_ROOT / 'wiki' / entity_type / f'{slug}.md'
    
    frontmatter = _build_frontmatter(fm_data)
    body = f'\n# {name}\n\n{content}\n' if content else f'\n# {name}\n'
    
    result = _write_file(file_path, frontmatter + body)
    print(f"Created: {result}")
    return result


def create_log(date, title, content, tags=None, project=None, surprise=None):
    """
    Create or append to a diary log entry.
    
    Args:
        date: ISO date string (YYYY-MM-DD)
        title: Log title (used in filename slug)
        content: Markdown body
        tags: List of tags
        project: Project name (added to frontmatter and tags)
        surprise: Optional surprise score (1-10)
    
    Returns:
        Path to created/updated file
    """
    tags = list(tags or [])
    if project and project not in tags:
        tags.append(project)
    
    year = date[:4]
    slug = _sanitize(title)
    
    # Check if a log for this date+project already exists
    diary_dir = BRAIN_ROOT / 'diary' / year
    diary_dir.mkdir(parents=True, exist_ok=True)
    
    existing = list(diary_dir.glob(f'{date}-*.md'))
    if project:
        project_logs = [f for f in existing if project in f.stem]
        if project_logs:
            # Append to existing log
            path = project_logs[0]
            current = path.read_text(encoding='utf-8')
            timestamp = datetime.now().strftime('%H:%M')
            current += f'\n\n## Update {timestamp}\n\n{content}\n'
            path.write_text(current, encoding='utf-8')
            print(f"Appended to: {path}")
            return path
    
    file_path = diary_dir / f'{date}-{slug}.md'
    
    fm_data = {
        'date': date,
        'type': 'log',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'created_with': 'brain-writer',
        'tags': tags,
    }
    if project:
        fm_data['project'] = project
    if surprise:
        fm_data['surprise'] = surprise
    
    frontmatter = _build_frontmatter(fm_data)
    body = f'\n# {title}\n\n{content}\n'
    
    result = _write_file(file_path, frontmatter + body)
    print(f"Created: {result}")
    return result


def create_diary(date, content, tags=None, source='manual', title=None, surprise=None):
    """
    Create a diary entry (personal/episodic).
    
    Args:
        date: ISO date string (YYYY-MM-DD)
        content: Markdown body
        tags: List of tags
        source: Origin of the entry (manual, read.ai, voice, etc.)
        title: Optional title
        surprise: Optional surprise score (1-10)
    
    Returns:
        Path to created file
    """
    tags = list(tags or [])
    year = date[:4]
    slug = _sanitize(title) if title else 'diary'
    
    file_path = BRAIN_ROOT / 'diary' / year / f'{date}-{slug}.md'
    
    fm_data = {
        'date': date,
        'type': 'diary',
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'created_with': 'brain-writer',
        'source': source,
        'tags': tags,
    }
    if surprise:
        fm_data['surprise'] = surprise
    
    frontmatter = _build_frontmatter(fm_data)
    heading = f'\n# {title}\n\n' if title else '\n'
    body = heading + content + '\n'
    
    result = _write_file(file_path, frontmatter + body)
    print(f"Created: {result}")
    return result


def create_todo(date, title, content, tags=None, priority='medium', due=None,
                project=None, budget=None):
    """
    Create a TODO file.
    
    Args:
        date: ISO date string (YYYY-MM-DD)
        title: TODO title
        content: Description
        tags: List of tags
        priority: low/medium/high/critical
        due: Due date (YYYY-MM-DD) or None
        project: Project name
        budget: Optional budget reference
    
    Returns:
        Path to created file
    """
    tags = list(tags or [])
    if project and project not in tags:
        tags.append(project)
    
    slug = _sanitize(title)
    file_path = BRAIN_ROOT / 'todo' / f'{date}-{slug}.md'
    
    fm_data = {
        'date': date,
        'type': 'todo',
        'status': 'open',
        'priority': priority,
        'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'created_with': 'brain-writer',
        'tags': tags,
    }
    if due:
        fm_data['due'] = due
    if project:
        fm_data['project'] = project
    if budget:
        fm_data['budget'] = budget
    
    frontmatter = _build_frontmatter(fm_data)
    body = f'\n# {title}\n\n{content}\n'
    
    result = _write_file(file_path, frontmatter + body)
    print(f"Created: {result}")
    return result


def update_file(file_path, content=None, frontmatter_updates=None, append=False):
    """
    Update an existing brain file.
    
    Args:
        file_path: Path to the file (relative to brain root or absolute)
        content: New content (replaces body, or appends if append=True)
        frontmatter_updates: Dict of frontmatter fields to update
        append: If True, append content instead of replacing
    
    Returns:
        Path to updated file
    """
    path = Path(file_path)
    if not path.is_absolute():
        path = BRAIN_ROOT / path
    
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    
    text = path.read_text(encoding='utf-8')
    
    # Split frontmatter and body
    match = re.match(r'^(---\n.*?\n---\n)(.*)', text, re.DOTALL)
    if match:
        fm_text, body = match.group(1), match.group(2)
    else:
        fm_text, body = '', text
    
    # Update frontmatter if requested
    if frontmatter_updates and fm_text:
        fm_match = re.match(r'^---\n(.*?)\n---', fm_text, re.DOTALL)
        if fm_match:
            fm_data = yaml.safe_load(fm_match.group(1)) or {}
            fm_data.update(frontmatter_updates)
            fm_data['last_updated'] = datetime.now().strftime('%Y-%m-%d')
            fm_text = _build_frontmatter(fm_data)
    
    # Update content
    if content is not None:
        if append:
            body = body.rstrip() + '\n' + content
        else:
            body = content
    
    path.write_text(fm_text + body, encoding='utf-8')
    print(f"Updated: {path}")
    return path
