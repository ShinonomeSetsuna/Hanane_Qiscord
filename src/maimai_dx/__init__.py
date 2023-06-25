"""Main module for maimaiDX."""

from src.maimai_dx.get_score import best_score
from src.maimai_dx.types import BestMaimai, MusicScore
from src.maimai_dx.query import query_music, query_music_by_uid
from src.maimai_dx.b50 import b50_generate
from src.maimai_dx.bind import bind_user, show_bind
