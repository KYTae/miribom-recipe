# 미리봄 레시피 사이트 데이터. 새 릴스가 나오면 VOLUMES 맨 앞에 하나 추가하고 build.py 실행.

VOLUMES = [
    {
        'slug': '16',
        'reel': 16,
        'type': 'tools',
        'part': 'AI TOOLS',
        'title': 'AI 초보 vs 고수, 쓰는 사이트 13',
        'short': '영상·이미지·목소리부터 3D·번역까지',
        'lede': '다들 쓰는 기본 기능 말고, AI 고수들이 분야마다 따로 쓰는 사이트를 모았어요. 2026년 10월 기준이에요.',
        'hero': '16-hero',
        'hero_shape': 'wide',
        'stat': ('기준', '26.10'),
        'groups': [],
        'tools': [('영상', '챗봇 앱에서 바로 생성', 'Kling 4.0', '여러 컷 연출에 음성·립싱크까지 한 번에', 'https://klingai.com', '16-01', 'X @Kling_ai'), ('이미지', '채팅창에 "그려줘"', 'Midjourney V8.2', '내 취향을 학습해서 미감이 달라요', 'https://www.midjourney.com', '16-02', 'X @midjourney'), ('이미지 편집', '무료 업스케일 사이트', 'Magnific', '캐릭터 생성·편집·업스케일을 한 곳에서', 'https://www.magnific.com', '16-03', 'X @magnific'), ('목소리', '편집앱 기본 TTS', 'ElevenLabs v3', '[속삭임] [웃음] 태그로 감정 연기', 'https://elevenlabs.io', '16-04', 'X @ElevenLabs'), ('음악', 'Suno 기본 모드', 'Suno Studio', '악기별로 쪼개서 다시 만드는 AI 작곡실', 'https://suno.com', '16-05', 'X @jerrod_lew'), ('더빙', '자막만 번역', 'sync.', '입모양까지 그 나라 말로 바꿔줘요', 'https://sync.so', '16-06', 'X @synclabs'), ('캐릭터 광고', '기본 아바타', 'Hedra', '캐릭터 하나로 광고 캠페인까지', 'https://www.hedra.com', '16-07', 'X @hedra_labs'), ('워크플로', '사이트마다 따로 돌리기', 'Figma Weave', '여러 AI를 노드로 연결해 한 번에', 'https://www.figma.com', '16-08', 'X @figma'), ('3D', '3D는 어렵다고 포기', 'Tripo', '사진 몇 장으로 3D 모델 완성', 'https://www.tripo3d.ai', '16-09', 'X @tripoai'), ('리서치', '그냥 검색', 'Perplexity', '출처 달린 리포트를 알아서 작성', 'https://www.perplexity.ai', '16-10', 'X @perplexity_ai'), ('자료 요약', '챗봇에 PDF 던지기', 'Gemini Notebook', '내 자료 안에서만 답해요 (구 NotebookLM)', 'https://notebooklm.google.com', '16-11', 'X @Gemini_Notebook'), ('웹사이트', '템플릿 사이트', 'Framer', '프롬프트로 만들고 바로 배포', 'https://www.framer.com', '16-12', 'X @framer'), ('번역', '번역기에 복붙', 'DeepL Voice', '회의 중 실시간 음성 번역', 'https://www.deepl.com', '16-13', 'X @DeepLcom')],
        'template': False,
    },
    {
        'slug': '15',
        'reel': 15,
        'part': 'PART 2',
        'title': 'AI 영상이 진짜가 되는 프롬프트 치트키 10',
        'short': '블랙박스 원테이크부터 같은 장면 다시 찍기까지',
        'lede': '조회수 6,414만 블랙박스 영상을 포함해, 원작자들이 공개한 Seedance 2.5 프롬프트에서 핵심 문장만 뽑았어요.',
        'hero': '15-hero',
        'hero_shape': 'tall',
        'stat': ('원작 조회', '6,414만'),
        'groups': [
            {
                'who': '@techhalla',
                'what': '블랙박스 콜라·멘토스 영상',
                'tool': 'GPT Image 2.5 → Seedance 2.5',
                'url': 'https://x.com/techhalla/status/2100526482212712584',
                'shape': 'tall',
                'items': [
                    ('01', '15-01', '첫 장면을 실사 이미지로 먼저 고정', 'lock the initial frame to a realistic one',
                     '바로 영상을 만들지 말고 <b>이미지 AI로 실사 같은 첫 장면을 먼저</b> 만든 뒤, 그 사진을 영상 AI 참조로 넣어요.'),
                    ('02', '15-02', '영화 말고 블랙박스 화질로', 'lived-in dashcam JPEG, not cinema, not HDR',
                     'AI 티가 나는 가장 큰 이유는 <b>너무 깨끗한 화질</b>이에요. 영화 느낌은 not으로 막아요.'),
                    ('03', '15-03', '초 단위로 사건 배치', '16-20s: [IT GOES] WHITE FOAM COLUMN',
                     '구간마다 무슨 일이 일어나는지 적으면 <b>클라이맥스가 원하는 타이밍에</b> 터져요. 원작에선 정확히 16초에 거품 기둥이 솟아요.'),
                    ('04', '15-04', '컷 없는 원테이크', 'CONTINUOUS SINGLE TAKE the entire 30s. Digital pinch-zooms only (no cuts).',
                     '컷 대신 <b>줌만 쓰는 한 번의 촬영</b>처럼 만들면 진짜 누가 찍은 영상 같아요.'),
                    ('05', '15-05', '인물·배경을 목록으로 고정', 'LOCKED CAST: (인물 설명)\nLOCKED SET: (장소·차량·소품)',
                     '<b>"No second person"</b>처럼 나오면 안 되는 것까지 적어서 엉뚱한 사람이 끼어드는 걸 막아요.'),
                ],
            },
            {
                'who': '@Scenario_gg',
                'what': '같은 영상을 다른 각도로 다시 찍기',
                'tool': 'Seedance 2.5 영상→영상 · 위 AI / 아래 원본',
                'url': 'https://x.com/Scenario_gg/status/2102365054389899695',
                'shape': 'stack',
                'items': [
                    ('06', '15-06', '내 영상의 연기·타이밍은 그대로', 'Do not restage, re-perform, re-time or reinterpret it.',
                     '내가 찍은 영상을 @video1로 넣고 이 문장을 쓰면 <b>움직임과 말하는 타이밍은 원본 그대로</b>예요.'),
                    ('07', '15-07', '바뀌는 건 카메라뿐', 'The only variable is camera position and lens.',
                     '같은 순간을 <b>다른 자리의 카메라로 다시 찍은 것처럼</b>. 원작자는 한 테이크로 13개 앵글을 만들었어요.'),
                    ('08', '15-08', '원본과 같은 속도로', 'Real time, 1:1 with @video1. No speed ramps, added slow motion, freeze frames or time remaps.',
                     'AI가 멋대로 <b>슬로모션을 넣는 걸</b> 막아서 원본 오디오와 입 모양이 어긋나지 않아요.'),
                ],
            },
            {
                'who': '@RishuaVR',
                'what': '인도네시아 골목 브이로그',
                'tool': 'Seedance 2.5',
                'url': 'https://x.com/RishuaVR/status/2089204108175741157',
                'shape': 'wide',
                'items': [
                    ('09', '15-09', '끝까지 같은 사람으로', 'Maintain consistent identity, clothing, hairstyle, and appearance throughout the entire video.',
                     '먼저 <b>나이·옷·피부·머리 모양까지</b> 자세히 묘사하고 이 문장을 붙여요.'),
                    ('10', '15-10', '일부러 흔들리게', 'DV camcorder aesthetic. Heavy handheld shake, frequent autofocus hunting. No stabilization. No cinematic camera moves.',
                     '손떨림·초점 흔들림을 넣고 매끈한 카메라는 막아서 <b>친구가 찍어준 브이로그</b> 느낌.'),
                ],
            },
        ],
        'template': True,
    },
    {
        'slug': '14',
        'reel': 14,
        'part': 'PART 1',
        'title': 'AI 영상 고수들만 아는 프롬프트 치트키 5',
        'short': '홈비디오, 게임 화면, 초 단위 샷까지',
        'lede': '조회수 수백만 AI 영상 다섯 편의 공개 프롬프트에서, 공통으로 들어간 한 문장씩을 뽑았어요.',
        'hero': '14-hero',
        'hero_shape': 'wide',
        'stat': ('원작 북마크', '1.1만+'),
        'groups': [
            {'who': '@Sheldon056', 'what': '홈비디오', 'tool': 'Seedance 2.5', 'url': 'https://x.com/Sheldon056', 'shape': 'wide',
             'items': [('01', '14-01', '연출 없는 홈비디오처럼', 'documentary-style personal home video',
                        'spontaneous, imperfect를 같이 쓰면 <b>진짜 일상</b> 같아요.')]},
            {'who': '@_VVSVS', 'what': '게임 화면', 'tool': 'Midjourney 8.2 + Seedance 2.5', 'url': 'https://x.com/_VVSVS', 'shape': 'wide',
             'items': [('02', '14-02', '게임 화면처럼', 'gameplay capture, rigid follow camera, flat exposure, deep focus, no film grain',
                        '카메라를 <b>게임 카메라</b>로 묘사해요.')]},
            {'who': '@SyntheSarah', 'what': '4K 숲', 'tool': 'Seedance 2.5', 'url': 'https://x.com/SyntheSarah', 'shape': 'wide',
             'items': [('03', '14-03', '초 단위로 샷 나누기', '0-4s: wide shot / 4-8s: medium shot / 8-12s: close-up',
                        '한 영상 안에 <b>여러 컷이 자연스럽게</b> 이어져요.')]},
            {'who': '@laviniavelle', 'what': '구름 마을', 'tool': 'Seedance 2.5', 'url': 'https://x.com/laviniavelle', 'shape': 'wide',
             'items': [('04', '14-04', '끌어올리며 공개', 'slowly pull the camera upward and reveal',
                        '카메라가 올라가며 전체가 드러나서 <b>스케일이 커져요</b>.')]},
            {'who': '@AIwithkhan', 'what': '가면 군중', 'tool': 'Seedance 2.5', 'url': 'https://x.com/AIwithkhan', 'shape': 'wide',
             'items': [('05', '14-05', '참조 이미지로 인물 고정', 'use the uploaded images as exact visual references',
                        '참조 이미지를 정확한 기준으로 지정하면 <b>인물·의상이 안 바뀌어요</b>.')]},
        ],
        'template': False,
    },
]

TEMPLATE = """[STYLE + CAMERA]
Vertical 9:16 smartphone video. lived-in phone footage, not cinema, not HDR.
CONTINUOUS SINGLE TAKE the entire 10s. Digital pinch-zooms only (no cuts).

[LOCKED CAST]
(인물: 나이, 옷, 피부, 머리 모양까지 자세히)
Maintain consistent identity, clothing, hairstyle, and appearance throughout the entire video.

[LOCKED SET]
(장소: 배경, 소품, 날씨, 시간대)
(나오면 안 되는 것: No second person, No billboards…)

[TIMELINE]
0-3s: [HOOK] (첫 장면, 바로 눈길 끄는 사건)
3-7s: (전개)
7-10s: [IT GOES] (클라이맥스)

[AVOID]
No stabilization. No cinematic camera moves. No modern color grading."""
