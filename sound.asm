	;;---CODE START---;;

	.inesprg 1
	.inesmap 0
	.inesmir 1
	.ineschr 0  ; note that we have no CHR-ROM bank in this code
	
	.bank 1
	.org $FFFA
	.dw 0 ; no VBlank routine
	.dw Start 
	.dw 0 ; we'll get to this at a later time

	.bank 0
	.org $8000

; C = 261.63 Hz
; raw period = 111860.8/frequency - 1

; note that I just copy/pasted code from the register sections
Start:
    jsr init_apu

    ; sweep
    ;lda #$ff
    ;sta $4001
    
    lda #170
    sta $4002

    lda #1
    sta $4003

    lda #%10111111
    sta $4000

infinite:
	jmp infinite

init_apu:
        ; Init $4000-4013
        ldy #$13
.loop:  lda .regs,y
        sta $4000,y
        dey
        bpl .loop
 
        ; We have to skip over $4014 (OAMDMA)
        lda #$0f
        sta $4015
        lda #$40
        sta $4017
   
        rts
.regs:
        .byte $30,$08,$00,$00
        .byte $30,$08,$00,$00
        .byte $80,$00,$00,$00
        .byte $30,$00,$00,$00
        .byte $00,$00,$00,$00


	;;--- END OF CODE FILE ---;;