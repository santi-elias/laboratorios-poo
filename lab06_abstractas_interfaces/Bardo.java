/**
 * Clase Bardo - Personaje que usa música y palabras para apoyar al equipo.
 * Puede curar aliados (Sanador) pero NO usa magia directa.
 * Su instrumento y carisma determinan su efectividad.
 */
public class Bardo extends Personaje implements Sanador {

    private int poderCuracion;
    private String instrumento; // el instrumento que toca
    private int carisma;        // influye en el daño y la curación

    public Bardo(String nombre, int nivel, int puntosVida,
                 int poderCuracion, String instrumento, int carisma) {
        super(nombre, nivel, puntosVida);
        this.poderCuracion = poderCuracion;
        this.instrumento = instrumento;
        this.carisma = carisma;
    }

    // --- Métodos abstractos de Personaje ---

    @Override
    public void atacar() {
        int danio = calcularDanio();
        System.out.println("[" + nombre + "] aturde con su " +
                           instrumento.toLowerCase() + ". Daño: " + danio);
    }

    @Override
    public int calcularDanio() {
        // Daño base por nivel + bonus de carisma
        int danioBase = nivel * 10;
        int bonusCarisma = carisma / 2;
        return danioBase + bonusCarisma;
    }

    // --- Métodos de Sanador ---

    @Override
    public void curarAliado(Personaje aliado) {
        aliado.puntosVida += poderCuracion;
        System.out.println(nombre + " entona una melodía y cura a " + aliado.nombre +
                           " +" + poderCuracion + ". Vida: " + aliado.puntosVida);
    }

    @Override
    public int getPoderCuracion() {
        return poderCuracion;
    }

    // --- Getters propios ---

    public String getInstrumento() {
        return instrumento;
    }

    public int getCarisma() {
        return carisma;
    }

    @Override
    public String toString() {
        return super.toString() + " | Instrumento: " + instrumento;
    }
}
