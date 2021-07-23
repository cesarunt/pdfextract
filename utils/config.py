# Main parameteres and variables
from easydict import EasyDict as edict

# GLOBAL VARIABLES
# ----------------
BLOCK_NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
ALLOW_WORDS = ['contreras', 'alarcón', 'anak', 'moinuddin', 'ok']
BLOCK_WORDS_ES = ['resumen', 'author', 'recibido', 'universidad', 'Dirección', 'Electrónica', 'Facultad']
BLOCK_WORDS_EN = ['abstract', 'author', 'jurnal', 'Article ', 'university', 'College ']

# PATTERN OBJECTIVE (OBJE)
PATTERN_OBJE_ES = ['objetivo general', 'objetivo principal', 'propósito de este artículo es', 'propósito central es', 'objetivo fue', 'por lo expuesto', 'objetivo']
PATTERN_OBJE_EN = ['aims', 'aimed', 'study', 'Purpose', 'purpose', 'objective']

# METHODOLOGY
# ----------------------------------------------------------------------------------
# PATTERN METHODOLOGY (METH) long
PATTERN_METH_ES = ['metodología', 'métodos']
PATTERN_METH_EN = ['methodology', 'methods']

# PATTERN TYPE (TYPE) NOT USE
# PATTERN_TYPE_ES = ['tipo']
# PATTERN_TYPE_EN = ['type']

# PATTERN DESIGN (DESI) long
PATTERN_DESI_ES = ['diseño']
PATTERN_DESI_EN = ['design']

# PATTERN APPROACH (APPR) short (3)
PATTERN_APPR_ES = ['enfoque']
PATTERN_APPR_EN = ['approaches']

# PATTERN LEVEL (LEVE) short (5)
PATTERN_LEVE_ES = ['nivel']
PATTERN_LEVE_EN = ['level']
PATTERN_LEVE_APPL_ES = ['mejorar', 'evaluar', 'aplicar', 'mejora', 'evalua', 'aplica']
PATTERN_LEVE_APPL_EN = ['improve', 'enhance', 'raise', 'upgrade', 'evaluate', 'apply']
PATTERN_LEVE_PRED_ES = ['predecir', 'predice']
PATTERN_LEVE_PRED_EN = ['predict', 'predicts']
PATTERN_LEVE_EXPI_ES = ['explicar', 'causa', 'efecto', 'incidencia', 'implicancia', 'influencia']
PATTERN_LEVE_EXPI_EN = ['explain', 'cause', 'effect', 'incidence', 'implication', 'influence']
PATTERN_LEVE_RELA_ES = ['relación', 'asociación', 'correlación', 'comparar', 'relacion', 'asociacion', 'correlacion', 'compara']
PATTERN_LEVE_RELA_EN = ['relation', 'association', 'correlation', 'compare']
PATTERN_LEVE_DESC_ES = ['satisfacción  de', 'satisfacción de']
PATTERN_LEVE_DESC_EN = ['satisfaction  of', 'satisfaction of']
PATTERN_LEVE_EXPO_ES = ['entrevistas', 'discusiones', 'entrevista', 'discusión']
PATTERN_LEVE_EXPO_EN = ['interviews', 'discussions', 'interview', 'discussion']

# PATTERN APPROACH (APPR) long (3)
PATTERN_APPR_QUAN_ES = ['encuesta', 'cuestionario', 'baterías', 'escalograma', 'escala', 'inventario', 'pruebas', 'cotejo', 'rúbrica', 'signatura', 'diferencial']
PATTERN_APPR_QUAN_EN = ['survey', 'questionary', 'questionnaire', 'batteries', 'scalogram', 'scale', 'inventory', 'tests', 'test', 'collation', 'comparison', 'contrast', 'rubric', 'signature' 'differential']
PATTERN_APPR_QUAL_ES = ['entrevistas', 'entrevista', 'guía de observación', 'diario', 'fichas', 'ficha', 'bibliográficas', 'bibliográfica', 'plan de trabajo', 'grabadoras', 'grabadora', 'análisis de contenidos', 'anécdotas', 'autobiografías', 'cuaderno de notas', 'libretas', 'libreta', 'apuntes', 'notas', 'preguntas', 'relatos', 'técnicas proyectivas']
PATTERN_APPR_QUAL_EN = ['interviews', ' interview',' observation guide', 'guide', ' diary ', 'records', ' files', 'file', 'bibliographic', 'focus group', 'recorders',' recorder ',' analysis of contents', 'anecdotes',' autobiographies', 'notebooks', 'notebook',' notes', 'note',' questions', 'stories',' projective techniques' ]

# PATTERN SAMPLE (SAMP)
PATTERN_SAMP_ES = ['la muestra']
PATTERN_SAMP_EN = ['sample']

# PATTERN TOOLS (TOOL)
PATTERN_TOOL_ES = ['instrumentos', 'instrumento']
PATTERN_TOOL_EN = ['tools', 'tool']

__C = edict()
cfg = __C

# List
__C.LIST = edict()
__C.LIST.ALLOW_WORDS = ALLOW_WORDS
__C.LIST.BLOCK_NUMBERS = BLOCK_NUMBERS
__C.LIST.BLOCK_WORDS_ES = BLOCK_WORDS_ES
__C.LIST.BLOCK_WORDS_EN = BLOCK_WORDS_EN
__C.LIST.PATTERN_METH_ES = PATTERN_METH_ES
__C.LIST.PATTERN_METH_EN = PATTERN_METH_EN
__C.LIST.PATTERN_OBJE_ES = PATTERN_OBJE_ES
__C.LIST.PATTERN_OBJE_EN = PATTERN_OBJE_EN
# __C.LIST.PATTERN_TYPE_ES = PATTERN_TYPE_ES
# __C.LIST.PATTERN_TYPE_EN = PATTERN_TYPE_EN
__C.LIST.PATTERN_DESI_ES = PATTERN_DESI_ES
__C.LIST.PATTERN_DESI_EN = PATTERN_DESI_EN
__C.LIST.PATTERN_APPR_ES = PATTERN_APPR_ES
__C.LIST.PATTERN_APPR_EN = PATTERN_APPR_EN
__C.LIST.PATTERN_LEVE_ES = PATTERN_LEVE_ES
__C.LIST.PATTERN_LEVE_EN = PATTERN_LEVE_EN
__C.LIST.PATTERN_SAMP_ES = PATTERN_SAMP_ES
__C.LIST.PATTERN_SAMP_EN = PATTERN_SAMP_EN
# __C.LIST.PATTERN_TOOL_ES = PATTERN_TOOL_ES
# __C.LIST.PATTERN_TOOL_EN = PATTERN_TOOL_EN

# levels
__C.LIST.PATTERN_LEVE_APPL_ES = PATTERN_LEVE_APPL_ES
__C.LIST.PATTERN_LEVE_APPL_EN = PATTERN_LEVE_APPL_EN
__C.LIST.PATTERN_LEVE_PRED_ES = PATTERN_LEVE_PRED_ES
__C.LIST.PATTERN_LEVE_PRED_EN = PATTERN_LEVE_PRED_EN
__C.LIST.PATTERN_LEVE_EXPI_ES = PATTERN_LEVE_EXPI_ES
__C.LIST.PATTERN_LEVE_EXPI_EN = PATTERN_LEVE_EXPI_EN
__C.LIST.PATTERN_LEVE_RELA_ES = PATTERN_LEVE_RELA_ES
__C.LIST.PATTERN_LEVE_RELA_EN = PATTERN_LEVE_RELA_EN
__C.LIST.PATTERN_LEVE_DESC_ES = PATTERN_LEVE_DESC_ES
__C.LIST.PATTERN_LEVE_DESC_EN = PATTERN_LEVE_DESC_EN
__C.LIST.PATTERN_LEVE_EXPO_ES = PATTERN_LEVE_EXPO_ES
__C.LIST.PATTERN_LEVE_EXPO_EN = PATTERN_LEVE_EXPO_EN
# approaches
__C.LIST.PATTERN_APPR_QUAN_ES = PATTERN_APPR_QUAN_ES
__C.LIST.PATTERN_APPR_QUAN_EN = PATTERN_APPR_QUAN_EN
__C.LIST.PATTERN_APPR_QUAL_ES = PATTERN_APPR_QUAL_ES
__C.LIST.PATTERN_APPR_QUAL_EN = PATTERN_APPR_QUAL_EN