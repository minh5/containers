{{- define "common_deployment" }}
          env:
            - name: NAMESPACE
              valueFrom:
                fieldRef:
                  fieldPath: metadata.namespace
            - name: RELEASE_NAME
              value: "{{ .Release.Name }}"
          volumeMounts:
            - name: "{{ .Release.Name }}-spark-config"
              mountPath: /tmp/config
      volumes:
        - name: "{{ .Release.Name }}-spark-config"
          configMap:
            name: "{{ .Release.Name }}-spark-config"
{{- end -}}