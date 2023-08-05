from pangeamt_nlp.translation_model.translation_model_factory import (
    TranslationModelFactory,
)
import logging
from pangeamt_nlp.seg import Seg
from nteu_translation_engine.pipeline import Pipeline
from typing import Dict, List


class Engine:
    def __init__(self, config: Dict, log_file: str = None, dbug: bool = False):
        self._logging = log_file is not None
        if self._logging:
            lvl = logging.DEBUG if dbug else logging.INFO
            logging.basicConfig(
                handlers=[logging.FileHandler(log_file)],
                level=lvl,
                format="%(asctime)s :: %(levelname)s :: %(message)s"
            )
            self._logger = logging.getLogger("my_logger")
        else:
            self._logger = None
        self._config = config
        self._model = self.load_model()
        self._pipeline = Pipeline(config, self._logger)

    def log(self, message: str, level: str = logging.INFO):
        if self._logging:
            self._logger.log(level, message)

    def load_model(self):
        name = self._config["translation_model"]["name"]
        args = self._config["translation_model"]["args_decoding"]
        if self._config["translation_engine_server"]["gpu"]:
            args["gpu"] = 0
        model_path = self._config["translation_engine_server"]["model_path"]
        self.log(f"Loading -> {name} with arguments {args}.")
        translation_model = TranslationModelFactory.get_class(name)
        return translation_model(model_path, **args)

    async def translate(self, srcs: List):
        return self._model.translate(srcs)

    async def process_batch(self, batch: List, lock=None):
        srcs = []
        segs = []
        ans = []
        for src in batch:
            seg = Seg(src)
            await self._pipeline.preprocess(seg)
            srcs.append(seg.src)
            segs.append(seg)
        if lock is not None:
            async with lock:
                translations = await self.translate(srcs)
        else:
            translations = await self.translate(srcs)
        for translation, seg in zip(translations, segs):
            seg.tgt = seg.tgt_raw = translation
            await self._pipeline.postprocess(seg)
            ans.append(seg.tgt)
            self.log(
                f"Translated -> {seg.src_raw} -> {seg.src} "
                f"-> {seg.tgt_raw} -> {seg.tgt}"
            )
        return ans
