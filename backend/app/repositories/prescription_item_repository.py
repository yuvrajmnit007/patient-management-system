from sqlalchemy.orm import Session

from app.models.prescription_item import PrescriptionItem


class PrescriptionItemRepository:

    @staticmethod
    def create_item(
        database: Session, item: PrescriptionItem
    ) -> PrescriptionItem:
        database.add(item)
        database.commit()
        database.refresh(item)
        return item

    @staticmethod
    def create_items(
        database: Session, items: list[PrescriptionItem]
    ) -> list[PrescriptionItem]:
        database.add_all(items)
        database.commit()
        for item in items:
            database.refresh(item)
        return items

    @staticmethod
    def get_items_by_prescription(
        database: Session, prescription_id: int
    ) -> list[PrescriptionItem]:
        return (
            database.query(PrescriptionItem)
            .filter(PrescriptionItem.prescription_id == prescription_id)
            .all()
        )

    @staticmethod
    def delete_items(database: Session, prescription_id: int) -> None:
        (
            database.query(PrescriptionItem)
            .filter(PrescriptionItem.prescription_id == prescription_id)
            .delete()
        )
        database.commit()

    @staticmethod
    def replace_items(
        database: Session,
        prescription_id: int,
        items: list[PrescriptionItem],
    ) -> list[PrescriptionItem]:
        """Delete existing items and insert the new set. Used by update flow."""
        (
            database.query(PrescriptionItem)
            .filter(PrescriptionItem.prescription_id == prescription_id)
            .delete()
        )
        database.add_all(items)
        database.commit()
        for item in items:
            database.refresh(item)
        return items