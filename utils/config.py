from easydict import EasyDict as edict
import os

# PATH LOCAL
# GLOBAL_PATH = os.path.abspath(os.getcwd())
# PATH SERVER
GLOBAL_PATH = '/var/www/webApp/webApp'

# BLOCK AND ALLOW WORDS
BLOCK_NUMBERS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
# BLOCK_WORDS_ES = ['resumen', 'author', 'recibido', 'universidad', 'dirección', 'electrónica', 'ingeniería', 'facultad']
# block by text_parser
BLOCK_WORDS_ES = ['resumen', 'introducción', 'r e s u m e n']
BLOCK_WORDS_EN = ['abstract', 'resumen', 'introduction', 'a b s t r a c t']
BLOCK_AUTHOR_ES = ['recibido', 'aceptado', 'autor', 'clave:', 'keywords:', 'publicado', 'published', 'required', 'universidad', 'facultad', 'colegio', 'colegios', 'departamento', 'instituto', 'cuenta', 'magister', 'procedimientos', 'local', 'issn', 'http', 'www', '@', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
BLOCK_AUTHOR_EN = ['received', 'recibido', 'accepted', 'author', 'keywords', 'colleague', 'published', 'required', 'university', 'universidad', 'faculty', 'school', 'schools', 'departament', 'institute', 'account', 'magister', 'procedures', 'local', 'issn', 'http', 'www', '@', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']

# RESUMEN
PATTERN_ABST_ES = ['este estudio', 'sumario', 'resumen', 'r e s u m e n', 'abstract', 'a b s t r a c t', 'presente artículo', 'este artículo,', 'el propósito', 'pretende', 'palabras claves', 'palabras-clave', 'clave:', 'abstract', '©', '___']
PATTERN_ABST_EN = ['this study', 'summary', 'resumen', 'r e s u m e n', 'abstract', 'a b s t r a c t', 'this paper', 'this article,', 'the purpose', 'aims to', 'keywords', 'acknowledgments', 'key words', 'palabras-clave', 'clave:', 'resumen', 'dedication', '©', '___' ]

# METHODOLOGY
PATTERN_METHOD_ES = ['Metodología de Investigación', 'Metodología', 'MeTodología', 'METODOLOGÍA', 'Métodos', 'MÉTODOS', 'Método', 'MÉTODO', 'La metodología', 'Diseños y Métodos', 'Instrumentos', 'Resultados', 'RESULTADOS', 'Resultado', 'Los resultados', 'Data Analysis', 'Conclusiones', 'CONCLUSIONES', 'Tabla', 'Recomendaciones', 'Discusión', 'https', 'http']
PATTERN_METHOD_EN = ['Research methodology', 'Methodology', 'MeThodology', 'METHODOLOGY', 'Methods', 'METHODS', 'Method', 'METHOD', 'The methodology', 'Research Design', 'Tools', 'Results', 'RESULTS', 'Resultados', 'Result', 'The results', 'Estimation', 'Conclusions', 'CONCLUSIONS', 'Table', 'Findings', 'FINDINGS', 'Suggestions', 'Discussion', 'https', 'http']

PATTERN_SUBTIT_ES = ['Introducción', 'INTRODUCCIÓN', 'Introduction', 'INTRODUCTION']
PATTERN_SUBTIT_EN = ['Introduction', 'INTRODUCTION', 'Introducción', 'INTRODUCCIÓN']

# RESULTS
PATTERN_RESU_ES = ['Nuestros resultados', 'Los resultados', 'Resultados', 'RESULTADOS', 'Resultado', 'RESULTADO', 'Instrumentos', 'Métodos', 'CONCLUSIONES', 'Conclusiones', 'DISCUSIONES', 'Discusiones', 'DISCUSIÓN', 'Discusión', 'Figura', 'Recomendaciones', 'Sugerencias', 'Limitaciones']
PATTERN_RESU_EN = ['Our results', 'The results', 'Results', 'RESULTS', 'Result', 'RESULT', 'Tools', 'Measures', 'Methods', 'CONCLUSIONS', 'Conclusions', 'DISCUSSIONS', 'Discussions', 'DISCUSSION', 'Discussion', 'Data Analysis', 'Resultados', 'Tabla', 'Chart', 'Tabela', 'FINDINGS', 'Findings', 'Suggestions', 'Limitations']

# CONCLUSIONS
PATTERN_CONC_ES = ['Conclusiones', 'CONCLUSIONES', 'Conclusión', 'CONCLUSIÓN', 'Concluyendo', 'CONCLUYENDO', 'C O N C L U Y E N D O', 'conflicto', 'Referencias', 'REFERENCIAS', 'Notas Finales', 'NOTAS FINALES', 'Bibliografía', 'BIBLIOGRAFÍA', 'www', '& ', 'Limitaciones']
PATTERN_CONC_EN = ['Conclusions', 'CONCLUSIONS', 'Conclusion', 'CONCLUSION', 'Concluding', 'CONCLUDING', 'C O N C L U D I N G', 'conflict', 'References', 'REFERENCES', 'Endnotes', 'ENDNOTES', 'Limitations', '& ']

# PATTERN DOI (DOI)
PATTERN_DOI_XX = ['https://doi.org/', 'doi', 'https://']
PATTERN_ABST_BLOCK = ['issn','http']

# PATTERN ARTICLE (ARTI)
PATTERN_ARTI_ES = ['revista']
PATTERN_ARTI_EN = ['journal']

# PATTERN OBJECTIVE (OBJE)
PATTERN_OBJE_ES = ['el objetivo', 'objetivo general', 'objetivo principal', 'propósito', 'los objetivos']
PATTERN_OBJE_EN = ['objective', 'aims', 'aimed', 'purpose', 'the objectives']

# METHODOLOGY
# PATTERN METHODOLOGY (METH) long
PATTERN_METH_ES = ['metodología', 'diseño y métodos', 'métodos.', 'métodos']
PATTERN_METH_EN = ['methodology', 'methods', 'methods.', 'research methods', 'research method', 'research design']

# PATTERN TYPE (TYPE) NOT USE
PATTERN_TYPE_ES = ['tipo']
PATTERN_TYPE_EN = ['type']

# PATTERN DESIGN (DESI) long
PATTERN_DESI_ES = ['diseño', 'diseñar']
PATTERN_DESI_EN = ['design']

# PATTERN APPROACH (APPR) short (3)
PATTERN_APPR_ES = ['enfoque']
PATTERN_APPR_EN = ['approaches']

# PATTERN LEVEL (LEVE) short (5)
PATTERN_LEVE_ES = ['nivel']
PATTERN_LEVE_EN = ['level']
PATTERN_LEVE_APPL_ES = ['mejorar', 'evaluar', 'mejora', 'evalua']
PATTERN_LEVE_APPL_EN = ['improve', 'enhance', 'raise', 'evaluate']
PATTERN_LEVE_PRED_ES = ['pronosticar', 'predecir', 'predice']
PATTERN_LEVE_PRED_EN = ['predict', 'predicts']
PATTERN_LEVE_EXPI_ES = ['explicar', 'causa', 'efecto', 'incidencia', 'implicancia', 'influencia']
PATTERN_LEVE_EXPI_EN = ['explain', 'cause', 'effect', 'incidence', 'implication', 'influence']
PATTERN_LEVE_RELA_ES = ['relación', 'asociación', 'correlación', 'comparar']
PATTERN_LEVE_RELA_EN = ['relation', 'association', 'correlation', 'compare']
PATTERN_LEVE_DESC_ES = ['describir']
PATTERN_LEVE_DESC_EN = ['describe']
PATTERN_LEVE_EXPO_ES = ['entrevistas', 'discusiones', 'entrevista', 'discusión']
PATTERN_LEVE_EXPO_EN = ['interviews', 'discussions', 'interview', 'discussion']

# PATTERN APPROACH (APPR) long (3)
PATTERN_APPR_QUAN_ES = ['encuesta', 'cuestionario', 'baterías', 'escalograma', 'escala', 'inventario', 'pruebas', 'técnicas estadísticas', 'correlación', 'cotejo', 'rúbrica', 'signatura', 'diferencial']
PATTERN_APPR_QUAN_EN = ['survey', 'questionary', 'questionnaire', 'batteries', 'scalogram', 'scale', 'inventory', 'tests', 'test', 'collation', 'comparison', 'contrast', 'rubric', 'signature' 'differential']
PATTERN_APPR_QUAL_ES = ['entrevistas', 'entrevista', 'guía de observación', 'diario', 'fichas', 'ficha', 'plan de trabajo', 'grabadoras', 'grabadora', 'análisis de contenidos', 'anécdotas', 'autobiografías', 'cuaderno de notas', 'libretas', 'libreta', 'apuntes', 'preguntas', 'relatos', 'técnicas proyectivas']
PATTERN_APPR_QUAL_EN = ['interviews', ' interview',' observation guide', 'guide', ' diary ', 'records', ' files', 'file', 'focus group', 'recorders',' recorder ',' analysis of contents', 'anecdotes',' autobiographies', 'notebooks', 'notebook',' notes:', 'questions', 'stories','projective techniques' ]

# PATTERN SAMPLE (SAMP)
PATTERN_SAMP_ES = ['la muestra','muestra']
PATTERN_SAMP_EN = ['samples', 'sample', 'exemplo']

# PATTERN TOOLS (TOOL)
PATTERN_TOOL_ES = ['instrumentos', 'instrumento']
PATTERN_TOOL_EN = ['tools', 'tool']

# PATTERN RESULT (RESU)
# PATTERN_RESU_ES = ['resultados y análisis', 'resultados y discusión', 'siguientes resultados:', 'resultados:', 'resultados obtenidos', 'resultados']
# PATTERN_RESU_EN = ['results and discussion', 'result and discussion', 'results discussion', 'results obtained', 'findings', 'results']


__C = edict()
cfg = __C

# PROCESS 
__C.PROCESS = edict()
__C.PROCESS.USE_GPU = False

# Percentage to change if posible to process service
__C.PROCESS.LIMIT_CPU = 90

# FILES
__C.FILES = edict()
__C.FILES.GLOBAL_PATH = GLOBAL_PATH
__C.FILES.MAX_NUMPAGES = 40
# HANDLE IMAGES / VIDEOS
__C.FILES.MAX_CONTENT_LENGTH = 40 * 1024 * 1024
__C.FILES.UPLOAD_EXTENSIONS  = ["PDF", "pdf"]

__C.FILES.SINGLE_UPLOAD      = GLOBAL_PATH + '/files/single/upload'
__C.FILES.SINGLE_SPLIT       = GLOBAL_PATH + '/files/single/split'
__C.FILES.SINGLE_OUTPUT      = GLOBAL_PATH + '/files/single/output'
__C.FILES.SINGLE_FORWEB      = 'files/single/output'

__C.FILES.MULTIPLE_UPLOAD    = GLOBAL_PATH + '/files/multiple/upload'
__C.FILES.MULTIPLE_SPLIT     = GLOBAL_PATH + '/files/multiple/split'
__C.FILES.MULTIPLE_OUTPUT    = GLOBAL_PATH + '/files/multiple/output'
__C.FILES.MULTIPLE_FORWEB    = 'files/multiple/output'


# List
__C.LIST = edict()
__C.LIST.PATTERN_ABST_BLOCK = PATTERN_ABST_BLOCK
__C.LIST.BLOCK_NUMBERS = BLOCK_NUMBERS
__C.LIST.BLOCK_WORDS_ES = BLOCK_WORDS_ES
__C.LIST.BLOCK_WORDS_EN = BLOCK_WORDS_EN
__C.LIST.BLOCK_AUTHOR_ES = BLOCK_AUTHOR_ES
__C.LIST.BLOCK_AUTHOR_EN = BLOCK_AUTHOR_EN
__C.LIST.PATTERN_METH_ES = PATTERN_METH_ES
__C.LIST.PATTERN_METH_EN = PATTERN_METH_EN

__C.LIST.PATTERN_ABST_ES = PATTERN_ABST_ES
__C.LIST.PATTERN_ABST_EN = PATTERN_ABST_EN
__C.LIST.PATTERN_METHOD_ES = PATTERN_METHOD_ES
__C.LIST.PATTERN_METHOD_EN = PATTERN_METHOD_EN
__C.LIST.PATTERN_SUBTIT_ES = PATTERN_SUBTIT_ES
__C.LIST.PATTERN_SUBTIT_EN = PATTERN_SUBTIT_EN
__C.LIST.PATTERN_DOI_XX  = PATTERN_DOI_XX
__C.LIST.PATTERN_ARTI_ES = PATTERN_ARTI_ES
__C.LIST.PATTERN_ARTI_EN = PATTERN_ARTI_EN
__C.LIST.PATTERN_OBJE_ES = PATTERN_OBJE_ES
__C.LIST.PATTERN_OBJE_EN = PATTERN_OBJE_EN
__C.LIST.PATTERN_TYPE_ES = PATTERN_TYPE_ES
__C.LIST.PATTERN_TYPE_EN = PATTERN_TYPE_EN
__C.LIST.PATTERN_DESI_ES = PATTERN_DESI_ES
__C.LIST.PATTERN_DESI_EN = PATTERN_DESI_EN
__C.LIST.PATTERN_APPR_ES = PATTERN_APPR_ES
__C.LIST.PATTERN_APPR_EN = PATTERN_APPR_EN
__C.LIST.PATTERN_LEVE_ES = PATTERN_LEVE_ES
__C.LIST.PATTERN_LEVE_EN = PATTERN_LEVE_EN
__C.LIST.PATTERN_SAMP_ES = PATTERN_SAMP_ES
__C.LIST.PATTERN_SAMP_EN = PATTERN_SAMP_EN
__C.LIST.PATTERN_TOOL_ES = PATTERN_TOOL_ES
__C.LIST.PATTERN_TOOL_EN = PATTERN_TOOL_EN
__C.LIST.PATTERN_RESU_ES = PATTERN_RESU_ES
__C.LIST.PATTERN_RESU_EN = PATTERN_RESU_EN
__C.LIST.PATTERN_CONC_ES = PATTERN_CONC_ES
__C.LIST.PATTERN_CONC_EN = PATTERN_CONC_EN

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