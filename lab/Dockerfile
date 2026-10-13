FROM ats-10.2.0-lab:local

USER root
COPY conf/records.yaml /opt/ats/etc/trafficserver/records.yaml
COPY conf/remap.config /opt/ats/etc/trafficserver/remap.config
COPY conf/storage.config /opt/ats/etc/trafficserver/storage.config
COPY remap/rules /opt/ats/etc/trafficserver/rules
COPY remap/rules-noslash /opt/ats/etc/trafficserver/rules-noslash
COPY remap/rules-dollar /opt/ats/etc/trafficserver/rules-dollar
RUN chown nobody:nogroup \
        /opt/ats/etc/trafficserver/records.yaml \
        /opt/ats/etc/trafficserver/remap.config \
        /opt/ats/etc/trafficserver/storage.config \
        /opt/ats/etc/trafficserver/rules \
        /opt/ats/etc/trafficserver/rules-noslash \
        /opt/ats/etc/trafficserver/rules-dollar

USER nobody
CMD ["traffic_server"]
