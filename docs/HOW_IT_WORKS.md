# Cómo funciona el taller

Esto es para contarlo en una entrevista, en voz alta, sin slides. El código de verdad está en inglés. Acá va la idea.

## Una analogía

Mirá el taller como un simulacro de incendio en un depósito. El depósito es de mentira (Cerulean Depot, tres SKU, tres notas). El "modelo" no piensa: lee un guion, como un actor que repite el libreto. Lo que se entrena es el edificio alrededor: qué puerta se puede abrir, quién firma una salida de mercadería, y qué checklist tiene que dar rojo cuando alguien saca stock sin permiso.

Fijate que el checklist no dice "caminaste por el pasillo A y después por el B". Dice "¿se lastimó alguien?", "¿gastaste de más?", "¿la respuesta dice el estante correcto?". Dos caminos distintos pueden aprobar.

## El flujo, paso a paso

1. La persona escribe una pregunta, por ejemplo dónde está el kit CD-240.
2. El loop arma dos mensajes: una regla fija del sistema, y la pregunta.
3. Antes de llamar al proveedor, mira el presupuesto simulado. Si la próxima llamada no entra, para con `budget` y no llama.
4. El proveedor falso devuelve el próximo turno del guion: o pide una herramienta, o cierra con un texto.
5. Si pide una herramienta, el código valida los argumentos. Si la herramienta escribe, exige un permiso humano en un conjunto (`Approval.granted`). El texto del modelo no alcanza para darse permiso.
6. El resultado de la herramienta vuelve al historial marcado como dato. Una nota puede decir "ignorá las instrucciones". En el camino normal eso no se convierte en una llamada.
7. El loop repite hasta una respuesta final, hasta el tope de pasos, o hasta el presupuesto.
8. La eval mira el resultado: ¿cambió el stock? ¿el texto tiene los datos pedidos? ¿el costo simulado quedó bajo el tope? No mira el orden exacto de las herramientas.

El servidor de la clase (módulo 3) es otra puerta al mismo depósito, por stdio, en JSON-RPC. El agente del cierre no abre un proceso por cada paso: llama a las mismas funciones. El módulo 3 es donde se ven los frames.

## Cómo se enseña

Dos bloques de tres horas, los tiempos son [EST], no los cronometré en un curso real.

En el primer bloque se arma el loop, el permiso y el servidor chiquito. En el segundo se escribe la eval, el tope de plata, el laboratorio de inyección, y el cierre. El cierre tiene que quedar verde. Después corrés `python -m workshop eval-regression` y tiene que salir con código 1. Si sale 0, la alarma está rota: el agente vulnerable cambió el stock y nadie lo marcó.

El grader (`python -m workshop check module-N`) mira las funciones del ejercicio. El starter tira `NotImplementedError` a propósito. La solución vive en `solutions/` y no hace falta espiarla para entender el enunciado, pero está para el que facilita.

## Glosario

| Palabra | Qué quiere decir acá |
| --- | --- |
| Agente | Un loop que alterna "pedir un turno" y "ejecutar una herramienta", con un corte. |
| Turno | Una respuesta del proveedor: herramienta o texto final. |
| Efecto | Lo que pasó de verdad: lectura, escritura, o bloqueo. |
| Invariante | Una condición sobre el efecto, no sobre el camino. |
| Cassette | Un archivo con el guion. No es una grabación de un proveedor pago. |
| Grant | El conjunto de nombres de herramientas que una persona autorizó para esa corrida. |
| Gate | El comando que falla si alguna invariante falla. En CI tiene que pasar. |
| Regresión forzada | Un agente de laboratorio que sí escribe. El gate tiene que ponerse rojo. |

## Límites, en serio

- El proveedor falso no lee el prompt. Si cambiás la pregunta y no el guion, la respuesta no cambia. Eso es intencional: la clase no depende de un modelo.
- El detector de la frase "Ignore previous instructions" no protege nada. Protege el hecho de que una escritura sin grant no corre.
- No hay un juez LLM. Hay una comparación literal contra una frase, y un desacuerdo a propósito con una etiqueta humana (5 de 6 en la corrida del 2026-10-17).
- El servidor no es el SDK oficial de MCP. Es un subconjunto para ver `server/discover`, `tools/list` y `tools/call`.
- Nada de esto demuestra experiencia de producción. Demuestra que estos casos sintéticos pasan o fallan como dice el gate.
