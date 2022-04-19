FROM continuumio/miniconda3:4.7.12 AS app-base

ENV WORKPATH=/app

WORKDIR $WORKPATH
COPY . $WORKPATH/
RUN mount=type=cache,target=/opt/conda/pkgs \
    conda env update --name base --file $WORKPATH/enviroment.yml --prune && \
    conda clean --all -y
EXPOSE 8080

CMD ["python3", "app.py"]